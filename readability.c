#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    int scount=0;
    int wcount=0;
    int lcount=0;
    string s = get_string("Text:");
// sentence counter
    for (int i = 0, n = strlen(s); i < n; i++) {
        if ((s[i] == '.') || (s[i] == '?') || (s[i] == '!')) {
            scount=scount+1;
            if(s[i+1] != ' ') {
                wcount=wcount+1;
            }
        }
    }
// letter counter
    for (int i = 0, n = strlen(s); i < n; i++) {
        if (isalpha(s[i])) {
            lcount=lcount+1;
        }
    }
// word counter
    for (int i = 0, n = strlen(s); i < n; i++) {
        if ((s[i] == ' ') && (s[i+1] != ' ')) {
            wcount=wcount+1;
        }
    }
//    printf("scount %d\n",scount);
//    printf("lcount %d\n",lcount);
//    printf("wcount %d\n",wcount);

    float L = (100.0/wcount) * lcount;
    float S = (100.0/wcount) * scount;
//    printf("L %f\n",L);
//    printf("S %f\n",S);
    float ind = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(ind);
//    printf("Index %f",ind);
    if(index < 1) {
        printf("Before Grade 1\n");
    }
    else if(index >= 16) {
            printf("Grade 16+\n");
    }
    else{
        printf("Grade %d\n",index);
    }
}
