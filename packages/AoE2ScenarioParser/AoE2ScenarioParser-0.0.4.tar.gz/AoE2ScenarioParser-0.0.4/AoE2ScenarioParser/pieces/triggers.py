from AoE2ScenarioParser.pieces import aoe2_piece
from AoE2ScenarioParser.helper.retriever import Retriever
from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.pieces.structs.trigger import TriggerStruct


class TriggerPiece(aoe2_piece.AoE2Piece):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("Trigger Version", DataType("f64")),
            Retriever("Trigger instructions start", DataType("s8")),
            Retriever("Number of triggers", DataType("s32"), save_as="number_of_triggers"),
            Retriever("Trigger data", DataType(TriggerStruct), set_repeat="{number_of_triggers}"),
            Retriever("Trigger display order array", DataType("u32"), set_repeat="{number_of_triggers}"),
        ]

        super().__init__("Triggers", retrievers, parser_obj)
