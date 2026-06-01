"""Focused parser tests for ReAct agent action formats."""
from src.agent.agent import ReActAgent
from src.tools.travel_tools import estimate_trip_cost


def _agent() -> ReActAgent:
    agent = ReActAgent.__new__(ReActAgent)
    agent._tool_map = {"estimate_trip_cost": estimate_trip_cost}
    return agent


def test_extract_action_format():
    action = _agent()._extract_action('Action: estimate_trip_cost("Da Lat", 3, 2)')
    assert action == ("estimate_trip_cost", ("Da Lat", 3, 2))


def test_extract_xml_tool_call_format():
    content = """<tool_call>
<function>
<name>estimate_trip_cost</name>
<arguments>
{"people": 2, "destination": "Da Lat", "days": 3}
</arguments>
</function>
</tool_call>"""
    action = _agent()._extract_action(content)
    assert action == ("estimate_trip_cost", ("Da Lat", 3, 2))


def test_extract_invalid_xml_tool_call_returns_none(monkeypatch):
    monkeypatch.setattr("src.agent.agent.logger.log_event", lambda *args, **kwargs: None)
    content = """<tool_call>
<function>
<name>estimate_trip_cost</name>
<arguments>{not-json}</arguments>
</function>
</tool_call>"""
    assert _agent()._extract_action(content) is None
