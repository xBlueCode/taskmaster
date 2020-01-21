#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	int		byte_count = 64;
	char	data[64];
	FILE	*fd_rand;
	FILE	*fd_file;
	int		count;

	fd_rand = fopen("/dev/urandom", "r");
	fd_file = fopen("/tmp/file", "w");
	count = 0;
	while (count < 5)
	{
		fread(&data, 1, byte_count, fd_rand);
		fwrite(data, 1, sizeof(data), fd_file);
		usleep(1000000);
		count++;
	}
	fclose(fd_rand);
	fclose(fd_file);
}

