#include <cs50.h>
#include <stdio.h>


int main(void)
{
    int hight = 0;
    /*main check to see correct input*/
    while (hight <= 0 || hight >= 9)
    {
        hight = get_int("Please enter hight\n");
    }
    /* row */
    for (int i = hight; i != 0; i -= 1)
    {
        /*char*/
        for (int j = hight - i + 2; j <= hight; j += 1)
        {
            printf(" ");
        }
        for (int f = i; f <= hight; f += 1)
        {
            printf("#");
        }
        /*gap in middle*/
        printf("  ");
        for (int z = i; z <= hight; z += 1)
        {
            printf("#");
        }
        printf("\n");
    }
}
