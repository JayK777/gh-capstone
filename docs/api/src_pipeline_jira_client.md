# `src.pipeline.jira_client`

JIRA client: fetch and parse user stories via JIRA REST API v2.

---

## class `JiraStory`

Parsed representation of a JIRA user story.

## class `JiraClient`

Wrapper around the JIRA REST API v2 for fetching user stories.

### `get_story(self, issue_key)`

Fetch a JIRA issue and return a JiraStory.
