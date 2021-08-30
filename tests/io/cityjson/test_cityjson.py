from tests.data.files import DatasetStats, railway_dataset, railway_dataset_stats
from metacity.io.cityjson.parser import CJParser
from collections import defaultdict


def count_gtypes(parser):
    gtypes = defaultdict(lambda: 0)
    for o in parser.parsed_objects:
        for g in o.geometry:
            gtypes[g.type] += 1
    return gtypes


def test_load(railway_dataset, railway_dataset_stats: DatasetStats):
    stats = railway_dataset_stats
    parser = CJParser(railway_dataset)
    parser.parse()
    gtypes = count_gtypes(parser)
    
    assert parser.is_empty == False
    assert len(parser.parsed_objects) == stats.obj_count
    assert stats.gtypes == gtypes


