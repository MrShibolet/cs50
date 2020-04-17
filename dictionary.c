// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

#include <stdlib.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
int count = 0;

// Number of buckets in hash table
const unsigned int N = 1;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int n = strlen(word) + 1;
    char temp[n];

    //terminator
    temp[n - 1] = '\0';

    for (int i = 0; i < n - 1; i += 1)
    {
        temp[i] = tolower(word[i]);
    }

    int index = hash(temp) % N;
    node *head = table[index];

    if (head != NULL)
    {
        node *tester = head;

        while (tester != NULL)
        {
            if (strcmp(temp, tester -> word) == 0)
            {
                //word in dict
                return true;
            }
            //advance tester
            tester = tester -> next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // lose lose hash function
    unsigned int hash = 0;
    int i;

    while ((i = *word++))
    {
        hash += i;
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    //Open dictionary
    FILE *fi = fopen(dictionary, "r");
    if (!fi)
    {
        fclose(fi);
        return false;
    }
    //buffer string for each word
    char buffer[LENGTH + 1];
    //while fgets doest get EOF from file fi
    while (fgets(buffer, (LENGTH + 2), fi) != NULL)
    {
        // add termination /0 at the end of the new string
        buffer[strlen(buffer) - 1] = '\0';
        int index = hash(buffer) % N;
        //temporary node test before insert into real
        node *temp = malloc(sizeof(node));
        if (!temp)
        {
            fclose(fi);
            return false;
        }
        //string copy pointer
        strcpy(temp -> word, buffer);
        temp -> next = table[index];
        //copy actual word into table
        table[index] = temp;
        count += 1;

    }
    fclose(fi);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // N is bucket size
    for (int i = 0; i <= N; i += 1)
    {
        node *tester = table[i];
        //while tester isnt empty
        while (tester != NULL)
        {
            //create pointer to old entry
            node *temp = tester;
            // advance tester
            tester = tester -> next;
            // free old
            free(temp);
        }
    }
    return true;
}
