# include <stdio.h>
# include <string.h>
struct Node{
    int flag1;
int content[8];
int flag2;
int flag3;};
void func(int idx, int type){
    struct Node node;
node.flag1 = 1;
node.flag2 = 1;
node.flag3 = 1;
memset(node.content, 0, 8 * sizeof(int));
if (idx > 8)
  return;
node.content[idx] = type; if (node.flag1 == 0)
printf("flag1\n"); if (node.flag2 == 0)
printf("flag2\n"); if (node.flag3 == 0)
printf("flag3\n"); if (node.content[2] == 1)
printf("content\n");}
main()
{
/ *Write
C
code in this
online
editor and run
it. * /
printf("Hello, World! \n");

return 0;
}