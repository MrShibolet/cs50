#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
//open file
    int i = 1;
    FILE *img = NULL;
//create "sting" with malloc (remember to free!!)
    char *filename = malloc(8 * sizeof(char));
//check argc
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
// check file for null
    if (!file)
    {
        return 1;
    }
//count length in bytes(Chars) till EOF
    int length = 0;
    while (fgetc(file) != EOF)
    {
        length += 1;
    }
//calculate blocks
    int blocks = length / 512;
//open file again because data is lost because of fgetc
    file = fopen(argv[1], "r");
//loop over all blocks
    for (int j = 0; j < blocks; j += 1)
    {
        BYTE now[512];
        fread(now, 1, 512, file);
//if header
        if (now[0] == 0xff && now[1] == 0xd8 && now[2] == 0xff && ((now[3] & 0xf0) == 0xe0))
        {
//check first time
            if (i == 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", i - 1);
            img = fopen(filename, "w");
            fwrite(now, sizeof(BYTE), 512, img);
            i += 1;
        }
        else if (i > 1)
        {
//writes data
            fwrite(now, sizeof(BYTE), 512, img);
        }
    }
// free and close everything
    fclose(file);
    fclose(img);
    free(filename);
}
