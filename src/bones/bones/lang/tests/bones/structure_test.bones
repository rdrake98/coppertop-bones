'(md-module_doc)
This file is designed to allow the structural parser to be tested.
'

// embedded: starts: '( ends:'  escape: \' - defaults to markdown for
'(imports)
a, b, c from module /dir1/file1
file1.d from module /dir1
module /dir1/file2
e from localFile1
f from ./subdir/localFile2
    {<:([)>}      // shouldn\'t fail here as "uses" isn\'t implemented yet
'

" a string with quotes \", literal backslash \\   tabs \t and new lines \n
it can be multi line and ([)  doesn't fail but expression separator is needed";

// {<:([)>} line comments \n and more

/* inline comment - ( [)   which would mean we could use code browser :) */

/* multi line
{<:([)>}
comment */

'(struct)B-SQL:accessors'    // type and method name is figured out
colNames:{[<:Table>x] ^ x `colNames};

x: select a, b+c by d from e where f>1, g !null >> xasc[`a];
[];
[a,b];
([{x}[1]]a. b. c);


'(test)'
{
    t: ([] a:`a);
    assert[
        a colName == `a
    ]
}


'(python-extension)
# embedding some other language or instructions
@bones
def fred(x,y):
    x + y
   # ([)
'

a: ("parenthesis have no " ,  (";" , " in them"));

{ [<:int>:a;<:list(int)>:b] '!(md-doc) answers a fred'
    a: (fred[a;b;] * c);
    t: ([] a:(1;2;{(1;)}))
}

// default [] for methods is [:x], [:x;:y] or [:x;:y;:z] depending on number of variables


// do we need call by name?
