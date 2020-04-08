#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
// take every row one by one
    for (int i = 0; i < height ;i += 1)
    {
// take every pixel in each row one by one
        for(int j = 0; j < width ; j += 1 )
        {
// average all colors to create gray
            double blue = image[i][j].rgbtBlue;
            double green = image[i][j].rgbtGreen;
            double red = image[i][j].rgbtRed;
            double avg = ((blue + red + green )/3);
// put average into picture
            int av = round(avg);
            image[i][j].rgbtBlue = av;
            image[i][j].rgbtGreen = av;
            image[i][j].rgbtRed = av;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // take every row one by one
    for (int i = 0; i < height ;i += 1)
    {
// take every pixel in each row one by one
        for(int j = 0; j < width ; j += 1 )
        {
// get all values for pixel
            double originalBlue = image[i][j].rgbtBlue;
            double originalGreen = image[i][j].rgbtGreen;
            double originalRed = image[i][j].rgbtRed;
//sepia algorythm
            double sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue;
            double sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue;
            double sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue;
// make them int so bmp can use them
            int red = round(sepiaRed);
            int blue = round(sepiaBlue);
            int green = round(sepiaGreen);
// cap off at 255 value
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
// put into picture
            image[i][j].rgbtBlue = blue;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtRed = red;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE rev[height][width];
// take every row one by one
    for (int i = 0; i < height ;i += 1)
    {
// take every pixel in each row one by one
        for(int j = 0; j < width ; j += 1 )
        {
// get all values for pixel
            rev[i][width-1-j].rgbtBlue = image[i][j].rgbtBlue;
            rev[i][width-1-j].rgbtRed = image[i][j].rgbtRed;
            rev[i][width-1-j].rgbtGreen = image[i][j].rgbtGreen;
        }
        for(int z = 0; z < width ; z +=1)
        {
            image[i][z].rgbtBlue = rev[i][z].rgbtBlue;
            image[i][z].rgbtRed = rev[i][z].rgbtRed;
            image[i][z].rgbtGreen = rev[i][z].rgbtGreen;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
        RGBTRIPLE blur[height][width];
// take every row one by one
    for (int i = 0; i < height ;i += 1)
    {
// take every pixel in each row one by one
        for(int j = 0; j < width ; j += 1 )
        {
// get all values for pixel
            double devider = 0;
            double blurblue = 0;
            double blurred = 0;
            double blurgreen = 0;
// look for one line above , current and below line
            for (int z = -1; z <= 2; z ++)
            {
// look for one pixel before , current and after the pixel in question
                for (int x = -1; x <= 2; x ++)
                {
                    //if pixel is in bound 
                    if ((j + x <= width -1 )&&(i + z <= height - 1)&&(i + z > 0)&&(j + x > 0))
                    {
                        blurblue = blurblue + image[i+z][j+x].rgbtBlue;
                        blurgreen = blurgreen + image[i+z][j+x].rgbtGreen;
                        blurred = blurred + image[i+z][j+x].rgbtRed;
                        devider += 1 ;
                    }
                }
            }
            blur[i][j].rgbtBlue = round(blurblue / devider);
            blur[i][j].rgbtRed = round(blurred / devider);
            blur[i][j].rgbtGreen = round(blurgreen / devider);
        }
    }
    for (int i = 0; i < height ;i += 1)
    { 
//put input into output
        for(int z = 0; z < width; z +=1)
        {
            image[i][z].rgbtBlue = blur[i][z].rgbtBlue;
            image[i][z].rgbtRed = blur[i][z].rgbtRed;
            image[i][z].rgbtGreen = blur[i][z].rgbtGreen;
        }
    }
    return;
}
