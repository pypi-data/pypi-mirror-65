UPDATE `ENTRY` SET 
  CATEGORY = :category,
  INCIDENT = :incident, 
  NOTE = :note,
  TIMESTAMP = :timestamp, 
  MODIFIED = :modified 
WHERE
  ID = :id;
