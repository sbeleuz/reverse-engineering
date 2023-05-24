#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

unsigned int get_seed(char *path)
{
    struct stat stats;

    if (stat(path, &stats) != 0)
    {
        printf("Unable to get file properties.\n");
        exit(1);
    }

    long time = stats.st_mtim.tv_sec;
    return time ^ 0xDEADBEEF;
}

int get_offset(FILE *f)
{
    char *fmi_re_course = "esruoc_er_imf";

    char s[256];
    char ptr;
    int i = 0;

    fseek(f, -1, SEEK_END);
    while (1)
    {
        fread(&ptr, 1, 1, f);
        fseek(f, -2, SEEK_CUR);
        s[i++] = ptr;

        char *found = strstr(s, fmi_re_course);
        if (found)
        {
            return (found - s) + strlen(fmi_re_course);
        }
    }

    return -1;
}

void reverse_file(FILE *f_read, FILE *f_write)
{
    char ptr;

    fseek(f_read, 0, SEEK_END);
    int ft = ftell(f_read);

    int i = 0;
    while (i < ft)
    {
        i++;
        fseek(f_read, -i, SEEK_END);

        fread(&ptr, 1, 1, f_read);
        fwrite(&ptr, 1, 1, f_write);
    }
}

int main()
{
    char *path = "";

    unsigned int seed = get_seed(path);
    srand(seed);

    FILE *f_read = fopen(path, "r");
    FILE *f_write_temp = fopen("out_temp", "w+");
    FILE *f_write = fopen("out", "w");

    // number of bytes starting from "fmi_re_course"
    int offset = get_offset(f_read);

    // get encrypted file size
    fseek(f_read, 0, SEEK_END);
    int ft = ftell(f_read);
    fseek(f_read, 0, SEEK_SET);

    char ptr;
    int i = 0;

    while (i < ft - offset)
    {
        fread(&ptr, 1, 1, f_read);
        printf("%x ", ptr & 0xff);

        ptr -= rand();
        printf("%c\n", ptr);
        fwrite(&ptr, 1, 1, f_write_temp);

        i++;
    }

    reverse_file(f_write_temp, f_write);

    fclose(f_read);
    fclose(f_write_temp);
    fclose(f_write);

    return 0;
}