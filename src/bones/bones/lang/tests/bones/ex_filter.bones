

x is an agg - name, age
y is collection of name

{ x filter {[r] `name in _.y} }

{x filter [[r] r `name in y] }

{select from x where name in y}

{select(x, {[e]


goal - be more accessible than VBA

// python list conprehension
[r for r in x if r.name in y]


filter
select


// indexy - discourage
{x at (x `name contains y)}


// rangey - no far too complex



explicit outputs
where
in


positional outputs
named outputs - struct / dict

r2, m, c = data regress(,`height, `age`gender) `r2`m`c




