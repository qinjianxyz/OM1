from dataclasses import dataclass

from actions.base import Interface


@dataclass
class SubmissionReceiptInput:
    """
    Input interface for writing an OM1 event submission receipt.

    Parameters
    ----------
    agent_name : str
        Name of the OM1 agent.
    concept : str
        One-sentence project concept.
    modes : str
        Mode summary.
    mcp_tools : str
        MCP tools used.
    checklist : str
        Submission-readiness checklist.
    demo_script : str
        Short demo script.
    """

    agent_name: str = ""
    concept: str = ""
    modes: str = ""
    mcp_tools: str = ""
    checklist: str = ""
    demo_script: str = ""


@dataclass
class SubmissionReceipt(Interface[SubmissionReceiptInput, SubmissionReceiptInput]):
    """
    This action writes a local markdown receipt for the OM1 builder-event submission.
    """

    input: SubmissionReceiptInput
    output: SubmissionReceiptInput

