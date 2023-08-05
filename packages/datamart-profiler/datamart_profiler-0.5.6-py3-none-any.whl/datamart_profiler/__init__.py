import contextlib
from datetime import datetime
import logging
import math
import numpy
import os
import pandas
from pandas.errors import EmptyDataError
import prometheus_client
import random
import requests
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
import time
from urllib.parse import urlencode
import warnings

from .profile_types import identify_types
from . import types
from .warning_tools import ignore_warnings


__version__ = '0.5.6'


logger = logging.getLogger(__name__)


MAX_SIZE = 50000000  # 50 MB

N_RANGES = 3

RANDOM_SEED = 89

SPATIAL_RANGE_DELTA_LONG = 0.0001
SPATIAL_RANGE_DELTA_LAT = 0.0001

SAMPLE_ROWS = 20

MAX_UNCLEAN_ADDRESSES = 0.2  # 15%
MAX_ADDRESS_LENGTH = 90  # 90 characters
MAX_NOMINATIM_REQUESTS = 200


BUCKETS = [0.5, 1.0, 5.0, 10.0, 20.0, 30.0, 60.0, 120.0, 300.0, 600.0]

PROM_PROFILE = prometheus_client.Histogram(
    'profile_seconds', "Profile time",
    buckets=BUCKETS,
)
PROM_TYPES = prometheus_client.Histogram(
    'profile_types_seconds', "Profile types time",
    buckets=BUCKETS,
)
PROM_SPATIAL = prometheus_client.Histogram(
    'profile_spatial_seconds', "Profile spatial coverage time",
    buckets=BUCKETS,
)
PROM_NOMINATIM_REQS = prometheus_client.Counter(
    'profile_nominatim_reqs', "Queries to Nominatim",
)
PROM_NOMINATIM_REQ_TIME = prometheus_client.Histogram(
    'profile_nominatim_req_seconds', "Time for Nominatim to answer a query",
)


def mean_stddev(array):
    total = 0
    for elem in array:
        if elem is not None:
            total += elem
    mean = total / len(array)if len(array) > 0 else 0
    total = 0
    for elem in array:
        if elem is not None:
            elem = elem - mean
            total += elem * elem
    stddev = math.sqrt(total / len(array)) if len(array) > 0 else 0

    return mean, stddev


def get_numerical_ranges(values):
    """
    Retrieve the numeral ranges given the input (timestamp, integer, or float).

    This performs K-Means clustering, returning a maximum of 3 ranges.
    """

    if not len(values):
        return []

    logger.info("Computing numerical ranges, %d values", len(values))

    clustering = KMeans(n_clusters=min(N_RANGES, len(values)),
                        random_state=0)
    values_array = numpy.array(values).reshape(-1, 1)
    with ignore_warnings(ConvergenceWarning):
        clustering.fit(values_array)
    logger.info("K-Means clusters: %r", list(clustering.cluster_centers_))

    # Compute confidence intervals for each range
    ranges = []
    sizes = []
    for rg in range(N_RANGES):
        cluster = [values[i]
                   for i in range(len(values))
                   if clustering.labels_[i] == rg]
        if not cluster:
            continue
        cluster.sort()
        min_idx = int(0.05 * len(cluster))
        max_idx = int(0.95 * len(cluster))
        ranges.append([
            cluster[min_idx],
            cluster[max_idx],
        ])
        sizes.append(len(cluster))
    logger.info("Ranges: %r", ranges)
    logger.info("Sizes: %r", sizes)

    # Convert to Elasticsearch syntax
    ranges = [{'range': {'gte': float(rg[0]), 'lte': float(rg[1])}}
              for rg in ranges]
    return ranges


def get_spatial_ranges(values):
    """
    Retrieve the spatial ranges (i.e. bounding boxes) given the input gps points.

    This performs K-Means clustering, returning a maximum of 3 ranges.
    """

    clustering = KMeans(n_clusters=min(N_RANGES, len(values)),
                        random_state=0)
    with ignore_warnings(ConvergenceWarning):
        clustering.fit(values)
    logger.info("K-Means clusters: %r", list(clustering.cluster_centers_))

    # Compute confidence intervals for each range
    ranges = []
    sizes = []
    for rg in range(N_RANGES):
        cluster = [values[i]
                   for i in range(len(values))
                   if clustering.labels_[i] == rg]
        if not cluster:
            continue
        cluster.sort(key=lambda p: p[0])
        min_idx = int(0.05 * len(cluster))
        max_idx = int(0.95 * len(cluster))
        min_lat = cluster[min_idx][0]
        max_lat = cluster[max_idx][0]
        cluster.sort(key=lambda p: p[1])
        min_long = cluster[min_idx][1]
        max_long = cluster[max_idx][1]
        ranges.append([
            [min_long, max_lat],
            [max_long, min_lat],
        ])
        sizes.append(len(cluster))
    logger.info("Ranges: %r", ranges)
    logger.info("Sizes: %r", sizes)

    # Lucene needs shapes to have an area for tessellation (no point or line)
    for rg in ranges:
        if rg[0][0] == rg[1][0]:
            rg[0][0] -= SPATIAL_RANGE_DELTA_LONG
            rg[1][0] += SPATIAL_RANGE_DELTA_LONG
        if rg[0][1] == rg[1][1]:
            rg[0][1] += SPATIAL_RANGE_DELTA_LAT
            rg[1][1] -= SPATIAL_RANGE_DELTA_LAT

    # TODO: Deal with clusters made of outliers

    # Convert to Elasticsearch syntax
    ranges = [{'range': {'type': 'envelope',
                         'coordinates': coords}}
              for coords in ranges]
    return ranges


def normalize_latlong_column_name(name, *substrings):
    name = name.lower()
    for substr in substrings:
        idx = name.find(substr)
        if idx >= 0:
            name = name[:idx] + name[idx + len(substr):]
            break
    return name


def pair_latlong_columns(columns_lat, columns_long):
    # Normalize latitude column names
    normalized_lat = {}
    for i, (name, values_lat) in enumerate(columns_lat):
        name = normalize_latlong_column_name(name, 'latitude', 'lat')
        normalized_lat[name] = i

    # Go over normalized longitude column names and try to match
    pairs = []
    missed_long = []
    for name, values_long in columns_long:
        norm_name = normalize_latlong_column_name(name, 'longitude', 'long')
        if norm_name in normalized_lat:
            pairs.append((columns_lat[normalized_lat.pop(norm_name)],
                          (name, values_long)))
        else:
            missed_long.append(name)

    # Gather missed columns and log them
    missed_lat = [columns_lat[i][0] for i in sorted(normalized_lat.values())]
    if missed_lat:
        logger.warning("Unmatched latitude columns: %r", missed_lat)
    if missed_long:
        logger.warning("Unmatched longitude columns: %r", missed_long)

    return pairs


def truncate_string(s, limit=140):
    """Truncate a string, replacing characters over the limit with "...".
    """
    if len(s) <= limit:
        return s
    else:
        # Try to find a space
        space = s.rfind(' ', limit - 20, limit - 3)
        if space == -1:
            return s[:limit - 3] + "..."
        else:
            return s[:space] + "..."


def nominatim_query(url, *, q):
    if url[-1] == '/':
        url = url [:-1]
    res = start = end = None  # Avoids warnings
    for i in range(5):
        if i > 0:
            time.sleep(1)
        PROM_NOMINATIM_REQS.inc()  # Count all requests
        start = time.perf_counter()
        res = requests.get(
            url +
            '/search?' +
            urlencode({'q': q, 'format': 'jsonv2'}),
        )
        end = time.perf_counter()
        if res.status_code not in (502, 503, 504):
            break
    res.raise_for_status()
    # Record time for successful request
    PROM_NOMINATIM_REQ_TIME.observe(end - start)
    if not res.headers['Content-Type'].startswith('application/json'):
        raise requests.HTTPError(
            "Response is not JSON for URL: %s" % res.url,
            response=res,
        )
    return res.json() or None


def nominatim_resolve_all(url, array, max_requests=MAX_NOMINATIM_REQUESTS):
    cache = {}
    locations = []
    not_found = 0  # Unique locations not found
    non_empty = 0
    start = time.perf_counter()
    processed = 0
    for processed, value in enumerate(array):
        value = value.strip()
        if not value:
            continue
        non_empty += 1

        if len(value) > MAX_ADDRESS_LENGTH:
            continue
        elif value in cache:
            if cache[value] is not None:
                locations.append(cache[value])
        else:
            location = nominatim_query(url, q=value)
            if location:
                loc = (
                    float(location[0]['lat']),
                    float(location[0]['lon']),
                )
                cache[value] = loc
                locations.append(loc)
            else:
                cache[value] = None
                not_found += 1
            if len(cache) >= max_requests:
                break
    logger.info(
        "Performed %d Nominatim queries in %fs (%d hits). Found %d/%d",
        len(cache),
        time.perf_counter() - start,
        len(cache) - not_found,
        len(locations),
        processed,
    )
    return locations, non_empty


@PROM_PROFILE.time()
def process_dataset(data, dataset_id=None, metadata=None,
                    lazo_client=None, nominatim=None,
                    search=False, include_sample=False,
                    coverage=True, plots=False, load_max_size=None, **kwargs):
    """Compute all metafeatures from a dataset.

    :param data: path to dataset, or file object, or DataFrame
    :param dataset_id: id of the dataset
    :param metadata: The metadata provided by the discovery plugin (might be
        very limited).
    :param lazo_client: client for the Lazo Index Server
    :param search: True if this method is being called during the search
        operation (and not for indexing).
    :param include_sample: Set to True to include a few random rows to the
        result. Useful to present to a user.
    :param coverage: Whether to compute data ranges (using k-means)
    :param plots: Whether to compute plots
    :param load_max_size: Target size of the data to be analyzed. The data will
        be randomly sampled if it is bigger. Defaults to `MAX_SIZE`, currently
        50 MB. This is different from the sample data included in the result.
    :returns: JSON structure (dict)
    """
    if 'sample_size' in kwargs:
        warnings.warn(
            "Argument 'sample_size' is deprecated, use 'load_max_size'",
            DeprecationWarning,
        )
        load_max_size = kwargs.pop('sample_size')
    if kwargs:
        raise TypeError(
            "process_dataset() got unexpected keyword argument %r" %
            next(iter(kwargs))
        )

    if not load_max_size:
        load_max_size = MAX_SIZE

    if metadata is None:
        metadata = {}

    data_path = None
    if isinstance(data, pandas.DataFrame):
        metadata['nb_rows'] = len(data)
        # FIXME: no sampling here!
    else:
        with contextlib.ExitStack() as stack:
            if isinstance(data, (str, bytes)):
                if not os.path.exists(data):
                    raise ValueError("data file does not exist")

                # saving path
                data_path = data

                # File size
                metadata['size'] = os.path.getsize(data)
                logger.info("File size: %r bytes", metadata['size'])

                data = stack.enter_context(open(data, 'rb'))
            elif hasattr(data, 'read'):
                # Get size by seeking to the end
                data.seek(0, 2)
                metadata['size'] = data.tell()
                data.seek(0, 0)
            else:
                raise TypeError("data should be a filename, a file object, or "
                                "a pandas.DataFrame")

            # Load the data
            try:
                if metadata['size'] > load_max_size:
                    # Sub-sample
                    logger.info("Counting rows...")
                    metadata['nb_rows'] = sum(1 for _ in data)
                    data.seek(0, 0)

                    ratio = load_max_size / metadata['size']
                    logger.info("Loading dataframe, sample ratio=%r...", ratio)
                    rand = random.Random(RANDOM_SEED)
                    data = pandas.read_csv(
                        data,
                        dtype=str, na_filter=False,
                        skiprows=lambda i: i != 0 and rand.random() > ratio)
                else:
                    logger.info("Loading dataframe...")
                    data = pandas.read_csv(data,
                                           dtype=str, na_filter=False)

                    metadata['nb_rows'] = data.shape[0]
            except EmptyDataError:
                logger.warning("Dataframe is empty!")
                metadata['nb_rows'] = 0
                metadata['nb_profiled_rows'] = 0
                metadata['columns'] = []
                return metadata

            logger.info("Dataframe loaded, %d rows, %d columns",
                        data.shape[0], data.shape[1])

    metadata['nb_profiled_rows'] = data.shape[0]

    # Get column dictionary
    columns = metadata.setdefault('columns', [])
    # Fix size if wrong
    if len(columns) != len(data.columns):
        logger.info("Setting column names from header")
        columns[:] = [{} for _ in data.columns]
    else:
        logger.info("Keeping columns from discoverer")

    # Set column names
    for column_meta, name in zip(columns, data.columns):
        column_meta['name'] = name

    if data.shape[0] == 0:
        logger.info("0 rows, returning early")
        return metadata

    # Lat / Long
    columns_lat = []
    columns_long = []

    # Textual columns
    column_textual = []

    # Addresses
    resolved_addresses = {}

    # Identify types
    logger.info("Identifying types, %d columns...", len(columns))
    with PROM_TYPES.time():
        for i, column_meta in enumerate(columns):
            logger.info("Processing column %d...", i)
            array = data.iloc[:, i]
            # Identify types
            structural_type, semantic_types_dict, additional_meta = \
                identify_types(array, column_meta['name'])
            # Set structural type
            column_meta['structural_type'] = structural_type
            # Add semantic types to the ones already present
            sem_types = column_meta.setdefault('semantic_types', [])
            for sem_type in semantic_types_dict:
                if sem_type not in sem_types:
                    sem_types.append(sem_type)
            # Insert additional metadata
            column_meta.update(additional_meta)

            # Compute ranges for numerical/spatial data
            if structural_type in (types.INTEGER, types.FLOAT):
                # Get numerical ranges
                numerical_values = []
                for e in array:
                    try:
                        e = float(e)
                    except ValueError:
                        e = None
                    else:
                        if not (-3.4e38 < e < 3.4e38):  # Overflows in ES
                            e = None
                    numerical_values.append(e)

                column_meta['mean'], column_meta['stddev'] = \
                    mean_stddev(numerical_values)

                # Compute histogram from numerical values
                if plots:
                    counts, edges = numpy.histogram(
                        [v for v in numerical_values if v is not None],
                        bins=10,
                    )
                    counts = [int(i) for i in counts]
                    edges = [float(f) for f in edges]
                    column_meta['plot'] = {
                        "type": "histogram_numerical",
                        "data": [
                            {
                                "count": count,
                                "bin_start": edges[i],
                                "bin_end": edges[i + 1],
                            }
                            for i, count in enumerate(counts)
                        ]
                    }

                # Get lat/long columns
                if types.LATITUDE in semantic_types_dict:
                    columns_lat.append(
                        (column_meta['name'], numerical_values)
                    )
                elif types.LONGITUDE in semantic_types_dict:
                    columns_long.append(
                        (column_meta['name'], numerical_values)
                    )
                elif coverage:
                    ranges = get_numerical_ranges(
                        [x for x in numerical_values if x is not None]
                    )
                    if ranges:
                        column_meta['coverage'] = ranges

            # Compute ranges for temporal data
            if (coverage or plots) and types.DATE_TIME in semantic_types_dict:
                timestamps = numpy.empty(
                    len(semantic_types_dict[types.DATE_TIME]),
                    dtype='float32',
                )
                for j, dt in enumerate(
                        semantic_types_dict[types.DATE_TIME]):
                    timestamps[j] = dt.timestamp()
                column_meta['mean'], column_meta['stddev'] = \
                    mean_stddev(timestamps)

                # Get temporal ranges
                if coverage:
                    ranges = get_numerical_ranges(timestamps)
                    if ranges:
                        column_meta['coverage'] = ranges

                # Compute histogram from temporal values
                if plots:
                    counts, edges = numpy.histogram(timestamps, bins=10)
                    counts = [int(i) for i in counts]
                    column_meta['plot'] = {
                        "type": "histogram_temporal",
                        "data": [
                            {
                                "count": count,
                                "date_start": datetime.utcfromtimestamp(
                                    edges[i],
                                ).isoformat(),
                                "date_end": datetime.utcfromtimestamp(
                                    edges[i + 1],
                                ).isoformat(),
                            }
                            for i, count in enumerate(counts)
                        ]
                    }

            # Compute histogram from categorical values
            if plots and types.CATEGORICAL in semantic_types_dict:
                counts = {}
                for value in array:
                    if not value:
                        continue
                    try:
                        counts[value] += 1
                    except KeyError:
                        counts[value] = 1
                counts = sorted(
                    counts.items(),
                    key=lambda p: p[1],
                )[:5]
                counts = sorted(counts)
                column_meta['plot'] = {
                    "type": "histogram_categorical",
                    "data": [
                        {
                            "bin": value,
                            "count": count,
                        }
                        for value, count in counts
                    ]
                }

            if structural_type == types.TEXT and \
                    types.DATE_TIME not in semantic_types_dict:
                column_textual.append(column_meta['name'])

            # Resolve addresses into coordinates
            if (
                nominatim is not None and
                structural_type == types.TEXT and
                types.TEXT in semantic_types_dict
            ):
                locations, non_empty = nominatim_resolve_all(
                    nominatim,
                    array,
                )
                if non_empty > 0:
                    unclean_ratio = 1.0 - len(locations) / non_empty
                    if unclean_ratio <= MAX_UNCLEAN_ADDRESSES:
                        resolved_addresses[column_meta['name']] = locations
                        if types.ADDRESS not in column_meta['semantic_types']:
                            column_meta['semantic_types'].append(types.ADDRESS)

    # Textual columns
    if lazo_client and column_textual:
        # Indexing with lazo
        if not search:
            # TODO: Remove previous data from lazo
            logger.info("Indexing textual data with Lazo...")
            try:
                if data_path:
                    # if we have the path, send the path
                    lazo_client.index_data_path(
                        data_path,
                        dataset_id,
                        column_textual
                    )
                else:
                    # if path is not available, send the data instead
                    for column_name in column_textual:
                        lazo_client.index_data(
                            data[column_name].values.tolist(),
                            dataset_id,
                            column_name
                        )
            except Exception:
                logger.error("Error indexing textual attributes from %s", dataset_id)
                raise
        # Generating Lazo sketches for the search
        else:
            logger.info("Generating Lazo sketches...")
            try:
                if data_path:
                    # if we have the path, send the path
                    lazo_sketches = lazo_client.get_lazo_sketch_from_data_path(
                        data_path,
                        "",
                        column_textual,
                    )
                else:
                    # if path is not available, send the data instead
                    lazo_sketches = []
                    for column_name in column_textual:
                        lazo_sketches.append(
                            lazo_client.get_lazo_sketch_from_data(
                                data[column_name].values.tolist(),
                                "",
                                column_name,
                            )
                        )
                # saving sketches into metadata
                for i in range(len(column_textual)):
                    n_permutations, hash_values, cardinality = \
                        lazo_sketches[i]
                    columns[i]['lazo'] = dict(
                        n_permutations=n_permutations,
                        hash_values=list(hash_values),
                        cardinality=cardinality,
                    )
            except Exception:
                logger.warning("Error getting Lazo sketches")
                raise

    # Lat / Lon
    if coverage:
        logger.info("Computing spatial coverage...")
        with PROM_SPATIAL.time():
            spatial_coverage = []
            pairs = pair_latlong_columns(columns_lat, columns_long)
            for (name_lat, values_lat), (name_long, values_long) in pairs:
                values = []
                for lat, long in zip(values_lat, values_long):
                    if (lat and long and  # Ignore None and 0
                            -90 < lat < 90 and -180 < long < 180):
                        values.append((lat, long))

                if len(values) > 1:
                    logger.info(
                        "Computing spatial ranges lat=%r long=%r (%d rows)",
                        name_lat, name_long, len(values),
                    )
                    spatial_ranges = get_spatial_ranges(values)
                    if spatial_ranges:
                        spatial_coverage.append({"lat": name_lat,
                                                 "lon": name_long,
                                                 "ranges": spatial_ranges})

            for name, values in resolved_addresses.items():
                logger.info(
                    "Computing spatial ranges address=%r (%d rows)",
                    name, len(values),
                )
                spatial_ranges = get_spatial_ranges(values)
                if spatial_ranges:
                    spatial_coverage.append({"address": name,
                                             "ranges": spatial_ranges})

        if spatial_coverage:
            metadata['spatial_coverage'] = spatial_coverage

    # Sample data
    if include_sample:
        rand = numpy.random.RandomState(RANDOM_SEED)
        choose_rows = rand.choice(
            len(data),
            min(SAMPLE_ROWS, len(data)),
            replace=False,
        )
        choose_rows.sort()  # Keep it in order
        sample = data.iloc[choose_rows]
        sample = sample.applymap(truncate_string)  # Truncate long values
        metadata['sample'] = sample.to_csv(index=False)

    # Return it -- it will be inserted into Elasticsearch, and published to the
    # feed and the waiting on-demand searches
    return metadata
