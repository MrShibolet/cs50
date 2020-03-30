#include <cs50.h>
#include <stdio.h>

long card;
int sum1=0;
int sum2=0;
int length=0;
int checksum=0;
int main(void)
{
    card = get_long("Please enter card number\n");
    /* checksum */
    for( long i = card ; i > 0; i=i/100){
        sum1 = sum1 + i%10;
    }
    for( long j = card*10 ; j > 0; j=j/100){
        sum2 = sum2 + j%10;
    }
    checksum = sum1 + sum2;    
    if(checksum%10 != 0){
        printf("INVALID");
    }
    else
    {
        for(long z = card; z > 0 ; z=z/10){
        length = length + 1;
    }
    if((length == 16 && card/1000000000000000%10 == 5)&&(card/100000000000000%10 >0 && card/100000000000000%10 <6)){
        printf("MasterCard");
    }
    else{
        if((length == 15 && card/100000000000000%10 == 3)&&(card/10000000000000%10 == 4 || card/10000000000000%10 == 7 )){
            printf("American Express");
        }
        else{
        if((length == 13 && card/1000000000000%10 == 4)||(length == 16 && card/1000000000000000%10 == 4)){
            printf("VISA");
        }
         else{
            printf("INVALID");     
            }
        }
    }
}
}

