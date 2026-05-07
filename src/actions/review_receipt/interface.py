from dataclasses import dataclass

from actions.base import Interface


@dataclass
class ReviewReceiptInput:
    """
    Input interface for writing an engineering review receipt.

    Parameters
    ----------
    verdict : str
        Short verdict string such as HONEST_PARTIAL or OK.
    decision : str
        Recommended decision or variant.
    evidence : str
        Evidence summary that supports the decision.
    limitation : str
        Honest limitation that must be carried into the demo.
    command : str
        Reproduction or verification command to show a reviewer.
    """

    verdict: str = ""
    decision: str = ""
    evidence: str = ""
    limitation: str = ""
    command: str = ""


@dataclass
class ReviewReceipt(Interface[ReviewReceiptInput, ReviewReceiptInput]):
    """
    This action writes a local markdown receipt with verdict, evidence, limitation,
    and reproduction command for the engineering review.
    """

    input: ReviewReceiptInput
    output: ReviewReceiptInput

