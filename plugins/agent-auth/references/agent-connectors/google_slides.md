Connect to Google Slides to create, read, and modify presentations programmatically.

Supports authentication: OAuth 2.0

## Table of Contents

- [Tool list](#tool-list)

---

## Tool list

## `googleslides_create_presentation`

Create a new Google Slides presentation with an optional title.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `schema_version` | string | No | Optional schema version to use for tool execution |
| `title` | string | No | Title of the new presentation |
| `tool_version` | string | No | Optional tool version to use for execution |

## `googleslides_read_presentation`

Read the complete structure and content of a Google Slides presentation including slides, text, images, shapes, and metadata.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | string | No | Fields to include in the response |
| `presentation_id` | string | Yes | The ID of the Google Slides presentation to read |
| `schema_version` | string | No | Optional schema version to use for tool execution |
| `tool_version` | string | No | Optional tool version to use for execution |
