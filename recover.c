#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
int i = 0;
FILE *img = NULL;
char *filename = malloc(8 * sizeof(char));
  if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        return 1;
    }
    int length = 0;
    while(fgetc(file) != EOF)
    {
        length += 1;
    }
    int blocks = length / 512;
    file = fopen(argv[1], "r");
    for (int j = 0; j < blocks; j += 1)
    {
        BYTE now[512];
        fread(now, 1, 512, file);
        if (now[0] == 0xff && now[1] == 0xd8 && now[2] == 0xff && ((now[3] & 0xf0) == 0xe0))
        {
            if(i == 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg",i);
            img = fopen(filename, "w");
            fwrite(now, sizeof(BYTE), 512, img);
            i += 1;
        }
        else if(i > 1)
        { 
            fwrite(now, sizeof(BYTE), 512, img); 
        }
    }
    fclose(file);
    fclose(img);
    free(filename);
}
