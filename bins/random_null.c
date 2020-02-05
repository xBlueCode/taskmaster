#include <stdio.h>
#include <stdlib.h>

int main()
{
	int		byte_count = 64;
	char	data[64];
	FILE	*fd_rand;
	FILE	*fd_null;

	fd_rand = fopen("/dev/urandom", "r");
	fd_null = fopen("/dev/null", "r");
	while (1)
	{
		fread(&data, 1, byte_count, fd_rand);
		fwrite(data, 1, sizeof(data), fd_null);
	}
}

