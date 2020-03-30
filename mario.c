#include <cs50.h>
#include <stdio.h>


int main(void)
{
    int hight = 0;
     while(hight <= 0 || hight >= 9){
     hight = get_int("Please enter hight\n");
     }
     /* row */
  for(int i=hight;i!=0;i-=1){
      /*char*/
    for(int j=hight-i;j<=hight;j+=1){
        printf(" ");
    }
    for(int f=i;f<=hight;f+=1)
    {
        printf("#");
        }
    printf("  ");
    for(int z=i;z<=hight;z+=1)
    {
        printf("#");
    }
    printf("\n");
  }
}
