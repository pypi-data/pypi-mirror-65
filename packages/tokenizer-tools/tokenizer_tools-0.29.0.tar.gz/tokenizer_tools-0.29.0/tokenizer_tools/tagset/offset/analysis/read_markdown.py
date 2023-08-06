import functools
import re
from typing import List
from urllib.parse import unquote

import mistune

from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.analysis.document_pattern import DocumentPattern
from tokenizer_tools.tagset.offset.analysis.entity_placeholder import EntityPlaceholder
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet


def create_doc(
    token_list: List[str], span_info_list: List[dict], placeholder_list, **kwargs
) -> Document:
    # span_info_list and placeholder_list only one
    if len(placeholder_list) == 0:
        document = Document(token_list)

        for k, v in kwargs.items():
            setattr(document, k, v)

        # 构建实体集合
        span_list = [
            Span(start=i["start"], end=i["end"], entity=i["type"])
            for i in span_info_list
        ]

        document.entities = SpanSet(span_list)

        return document
    else:
        doc_pattern = DocumentPattern(token_list)

        for k, v in kwargs.items():
            setattr(doc_pattern, k, v)

        # 构建实体集合
        span_list = [
            EntityPlaceholder(start=i["start"], end=i["end"], entity=i["type"])
            for i in placeholder_list
        ]

        doc_pattern.entities = SpanSet(span_list)

        return doc_pattern


def read_markdown(data) -> List[Document]:
    doc_parser = mistune.create_markdown(renderer=mistune.AstRenderer())
    doc = doc_parser(data)

    doc_list = []

    current_intent = None
    for top_item in doc:
        if top_item["type"] == "heading":  # this is a head
            # assert top_item["level"] == 1
            current_intent = top_item["children"][0]["text"]
        elif top_item["type"] == "list":  # this is ner list
            for sub_item in top_item["children"]:  # sub item in list
                assert sub_item["type"] == "list_item"

                token_list = []
                span_list = []
                placeholder_list = []

                for element in sub_item["children"]:
                    assert element["type"] == "block_text"

                    for span_set in element["children"]:
                        if span_set["type"] == "text":  # plain text
                            partial_token_list = list(span_set["text"])
                            token_list.extend(partial_token_list)

                        elif span_set["type"] == "link":
                            entity_type = unquote(span_set["link"])

                            assert len(span_set["children"]) == 1

                            assert span_set["children"][0]["type"] == "text"
                            entity_value = span_set["children"][0]["text"]

                            partial_token_list = list(entity_value)

                            start_index = len(token_list)

                            span_list.append(
                                {
                                    "start": start_index,
                                    "end": len(token_list) + len(partial_token_list),
                                    "type": entity_type,
                                }
                            )

                            token_list.extend(partial_token_list)

                        elif span_set["type"] == "codespan":
                            entity_placeholder = span_set["text"]

                            placeholder_list.append(
                                {
                                    "start": len(token_list),
                                    "end": len(token_list) + 1,
                                    "type": entity_placeholder,
                                }
                            )

                            token_list.extend([entity_placeholder])

                doc = create_doc(
                    token_list,
                    span_list,
                    placeholder_list=placeholder_list,
                    intent=current_intent,
                )

                doc_list.append(doc)

    return doc_list
