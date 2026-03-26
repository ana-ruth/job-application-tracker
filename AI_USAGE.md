# AI Usage Documentation

## Tools Used
Gemini

## Key Prompts
1. "Why is the dictionary from my flask route not displaying in the html?"
2. "How to display multiple rows from flask in html?"
3. "How to change my HTML structure to include an edit functionality for each row?"
4. "How to change the contacts route to send HTML a list with existing companies for dropdown?"
5. "What am I missing to make sure the dropdown automatically shows the current company when clicking edit?"
6. "What do I need to change in jobs page to display and get json data for requirements column?"
7. "How to get json data in a text area for applications table?"
8. "Why is the JSON data returning as a string and not as an list?"
9. "How to keep labels on top of inputs without using div in CSS?"

## What Worked Well
- AI provided possible causes for not displaying flask data in html
- Gave me an example of how to use {{% for %}}
- Gemini showed me how to do Server-Side Inline Edit in html
- It showed me that I should add to render_template() the list of companies from the select query. 
- Gemini showed me how to include if else logic and selected statements in the html dropdown options
- Gemini showed me needed changes in HTML and Flask code to convert data into json to update jobs table and how to get json data from table to display in the website
- AI showed me how to get and edit JSON data in a text area
- It gave me code to convert JSON string to a list in Python

## What I Modified
- Applied example to my own code based on the fields my tables have. 
- Added all remaining columns (table fields) from AI example to HTML, and updated flask route to get all fields for the update query
- I wrote the corresponding HTML form, to the given API route to display companies in the contacts insert form
- Changed table fields to the corresponding values for my table.
- Changed fields to match my keys in requirements json columns. Updated SQL queries for jobs table to include requirements column in insert, update, and read. 
- I included JSON text to list code in corresponding function 

## Lessons Learned
