k=QQ
S=k[x1,x2,x3,x4,x5,x6,x7,x8]
I=ideal(x1*x2,x2*x3,x3*x4,x4*x5,x5*x6,x6*x7,x7*x8)
d=(res I).dd
"output.json" <<(for i from 1 to pdim(module I)+1 when true list concatenate({"\"",toString(i),"\"",":",toString(for j from 0 to rank(target(d_i))-1 when true list concatenate({"\"",toString(j),"\"",":",toString(for l from 0 to rank(source(d_i))-1 when true list concatenate({"\"",toString(l),"\"",":",concatenate({"\"",toString(((entries (res I).dd_i)_j)_l),"\""})  }) do l)}) do j)}) do i)<< endl << close
