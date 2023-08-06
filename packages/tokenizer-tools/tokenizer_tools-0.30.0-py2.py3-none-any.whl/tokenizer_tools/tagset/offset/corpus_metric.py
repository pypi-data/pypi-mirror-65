from sklearn.metrics import confusion_matrix

from tokenizer_tools.tagset.offset import seqeval as seq_metrics


class CorpusMetric:
    """metrics for corpus between gold and predicted"""

    def __init__(
        self,
        intent_confusion_matrix,
        domain_confusion_matrix,
        entity_f1_score,
        entity_accuracy_score,
        entity_precision_score,
        entity_recall_score,
        entity_classification_report,
    ):
        super().__init__()

        self.intent_confusion_matrix = intent_confusion_matrix
        self.domain_confusion_matrix = domain_confusion_matrix
        self.entity_f1_score = entity_f1_score
        self.entity_accuracy_score = entity_accuracy_score
        self.entity_precision_score = entity_precision_score
        self.entity_recall_score = entity_recall_score
        self.entity_classification_report = entity_classification_report

    @classmethod
    def create_from_corpus(cls, true, pred):
        intent_confusion_matrix = cls._intent_confusion_matrix(true, pred)
        domain_confusion_matrix = cls._domain_confusion_matrix(true, pred)
        entity_f1_score = cls._entity_f1_score(true, pred)
        entity_accuracy_score = cls._entity_accuracy_score(true, pred)
        entity_precision_score = cls._entity_precision_score(true, pred)
        entity_recall_score = cls._entity_recall_score(true, pred)
        entity_classification_report = cls._entity_classification_report(true, pred)

        return cls(
            intent_confusion_matrix,
            domain_confusion_matrix,
            entity_f1_score,
            entity_accuracy_score,
            entity_precision_score,
            entity_recall_score,
            entity_classification_report,
        )

    @classmethod
    def _intent_confusion_matrix(cls, true, pred):
        return cls._attr_confusion_matrix(true, pred, "intent")

    @classmethod
    def _domain_confusion_matrix(cls, true, pred):
        return cls._attr_confusion_matrix(true, pred, "domain")

    @classmethod
    def _attr_confusion_matrix(cls, true, pred, attr):
        true_attr = [getattr(doc, attr) for doc in true]
        pred_attr = [getattr(doc, attr) for doc in pred]

        return confusion_matrix(true_attr, pred_attr)

    @classmethod
    def _entity_f1_score(cls, true, pred):
        return seq_metrics.f1_socre(true, pred)

    @classmethod
    def _entity_accuracy_score(cls, true, pred):
        return seq_metrics.accuracy_score(true, pred)

    @classmethod
    def _entity_precision_score(cls, true, pred):
        return seq_metrics.precision_score(true, pred)

    @classmethod
    def _entity_recall_score(cls, true, pred):
        return seq_metrics.recall_score(true, pred)

    @classmethod
    def _entity_classification_report(cls, true, pred):
        return seq_metrics.classification_report(true, pred)
