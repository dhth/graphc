MATCH (n:Person)
WHERE n.age > 25
RETURN n.name, n.age
ORDER BY n.age DESC