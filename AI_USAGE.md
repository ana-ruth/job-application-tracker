# AI Usage Documentation

## Tools Used
Gemini

## Key Prompts
1. "Why is the dictionary from my flask route not displaying in the html?"
2. "How to display multiple rows from flask in html?"
3. "How to change my HTML structure to include an edit functionality for each row?"
4. "How to change the contacts route to send HTML a list with existing companies for dropdown?"

## What Worked Well
- AI provided possible causes for not displaying flask data in html
- Gave me an example of how to use {{% for %}}
- Gemini showed me how to do Server-Side Inline Edit in html
- It showed me that I should add to render_template() the list of companies from the select query. 

## What I Modified
- Applied example to my own code based on the fields my tables have. 
- Added all remaining columns (table fields) from AI example to HTML, and updated flask route to get all fields for the update query
- I wrote the corresponding HTML form, to the given API route to display companies in the contacts insert form

## Lessons Learned
