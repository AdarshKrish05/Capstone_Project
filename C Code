#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

void Encrypt(int key,int rows,int len,char string[])
{
    char mat[rows][key];
    int k = 0;

    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<key;j++)
        {
            mat[i][j] = ' ';
        }
    }

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < key; j++)
        {
            if (k < len)
            {
                mat[i][j] = string[k++];
            }
        }
    }

    k=0;

    for(int i=0;i<key;i++)
    {
        for(int j=0;j<rows;j++)
        {
            string[k++] = mat[j][i];
        }
    }
}

void ceaser1(int key,char string[10000])
{
    int len = strlen(string);

    for(int i=0;i<len;i++)
    {
        if(string[i] == ' ')
        {
            string[i] = 'X';
        }
        else
        {
            if(isalpha(string[i]))
            {
                int base = isupper(string[i])?'A':'a';
                string[i] = (string[i] - base + key) % 26 + base;
            }
        }
    }
}

void ceaser2(int key,char string[10000])
{
    int len = strlen(string);

    for(int i=0;i<len;i++)
    {
        if(string[i] == 'X')
        {
            string[i] = ' ';
        }
        else
        {
            if(isalpha(string[i]))
            {
                int base = isupper(string[i]) ? 'A' : 'a';
                string[i] = (string[i] - base - key + 26) % 26 + base;
            }
        }
    }
}

void Decrypt(int key, int rows, char string[10000], int len) {
    char mat[rows][key];
    int k = 0;

    for (int i = 0; i < key; i++) {
        for (int j = 0; j < rows; j++) {
            if (k < len)
                mat[j][i] = string[k++];
        }
    }

    k = 0;

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < key; j++) {
            if (k < len)
                string[k++] = mat[i][j];
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s input_file output_file key encrypt/decrypt\n", argv[0]);
        return 1;
    }

    int key = atoi(argv[3]);
    if (key < 1 || key > 25) {
        fprintf(stderr, "Key must be between 1 and 25.\n");
        return 1;
    }

    FILE *fin = fopen(argv[1], "r");
    if (!fin) {
        perror("Error opening input file");
        return 1;
    }

    // Get file size
    fseek(fin, 0, SEEK_END);
    long fsize = ftell(fin);
    fseek(fin, 0, SEEK_SET);

    // Allocate buffer
    char *str = malloc(fsize + 1);
    if (!str) {
        fclose(fin);
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Read file
    size_t bytes_read = fread(str, 1, fsize, fin);
    str[bytes_read] = '\0';
    fclose(fin);

    int len = strlen(str);
    int rows = (int)ceil((double)len / key);

    if (strcmp(argv[4], "decrypt") == 0) {
        Decrypt(key, rows, str, len);
        ceaser2(key, str);
    } else {
        ceaser1(key, str);
        Encrypt(key, rows, len, str);
    }

    FILE *fout = fopen(argv[2], "w");
    if (!fout) {
        perror("Error opening output file");
        free(str);
        return 1;
    }

    fputs(str, fout);
    fclose(fout);
    free(str);

    return 0;
}
