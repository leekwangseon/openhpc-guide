#include <mpi.h>
#include <stdio.h>
int main(int argc, char **argv) {
    int rank, size, length, sum;
    char host[MPI_MAX_PROCESSOR_NAME];
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(host, &length);
    MPI_Allreduce(&rank, &sum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    printf("rank=%d size=%d host=%s sum=%d\n", rank, size, host, sum);
    MPI_Finalize();
    return sum == size * (size - 1) / 2 ? 0 : 1;
}
