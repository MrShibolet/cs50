#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // no argument fix
    if (argc == 1)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
// counter to check validity
    int countester = 0;
    string argv1 = argv[1];
    for (int j = 0; j <= strlen(argv[1]) - 1; j += 1)
    {
        if (isdigit(argv1[j]) == 0)
        {
            countester += 1;
        }
    }
// see if program actually works
    if ((argc == 2) && (countester == 0))
    {
        string text = get_string("plaintext:");
        char cypher[strlen(text)];
        int key = atoi(argv[1]);
        // handles large numbers
        key = key % 26;
        // loop for each char in input key
        for (int i = 0; i <= strlen(text); i++)
        {
            //checks if char is alpha
            if (isalpha(text[i]))
            {
                // testing for correct looping
                if ((isupper(text[i] + key) == isupper(text[i])) && isalpha(text[i] + key))
                {
                    cypher[i] = text[i] + key;
                }
                else
                {
                    cypher[i] = text[i] - 26 + key;
                }
            }
            else
            {
                cypher[i] = text[i];
            }
        }
        printf("ciphertext: %s\n", cypher);
    }
    //if argument is not valid come here
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    return 0;
}



