#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

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
        }
    }
// letter counter
    for (int i = 0, n = strlen(s); i < n; i++) {
        if (isalpha(s[i])) {
            lcount=lcount+1;
        }
    }
// word counter
    if (s[strlen(s)-1] != ' ') {
        wcount+=1;
    }
    for (int i = 0, n = strlen(s); i < n; i++) {
        if ((s[i] == ' ') && (s[i+1] != ' ')) {
            wcount=wcount+1;
        }
    }
    int L = (100/wcount) * lcount;
    int S = (100/wcount) * scount;
    int index = 0.0588 * L - 0.296 * S - 15.8;
    if(index < 1) {
        printf("Before Grade 1");
    }
    else if(index > 16) {
            printf("Grade 16+");
    }
    else{
        printf("Grade %d",index);
    }
}
