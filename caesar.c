#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,string argv[])
{
    int countester = 0;
    string argv1 = argv[1];
    string text = "zzZZ";
    for(int j = 0; j <= strlen(argv[1]) - 1; j+=1)
    {
       if(isdigit(argv1[j]) == 0)
        {
            countester += 1;
        }
    }
    if ((argc == 2) && (countester == 0))
    {
        char cypher[strlen(text)];
        int key = atoi(argv[1]);
        key = key%26;
        printf("cipher:  %d\n",key);
        for(int i = 0; i <= strlen(text);i++)
        {
            if(isalpha(text[i]))
            {
                if ((text[i] == 'z') || (text[i] == 'Z'))
                {
                    cypher[i] = text[i] - 26 + key;
                }
                else
                {
                    cypher[i] = text[i] + key;
                }
            }
            else
            {
                cypher[i] = text[i];
            }
        }
        printf("ciphertext: %s\n",cypher);
    }
    else{
        printf("Usage: ./caesar key\n");
    }
return 0;
}



