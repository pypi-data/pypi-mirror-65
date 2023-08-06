import ndtreepy.ndfunc as ndfunc

def indent_show_tree(tree,k='_id'):
    sdfs = ndfunc.tree2sdfs(tree)
    for i in range(len(sdfs)):
        indents = '    ' * ndfunc.get_depth(tree,sdfs[i])
        an = sdfs[i][k]
        print('['+str(i)+']'+indents+str(an))


        
