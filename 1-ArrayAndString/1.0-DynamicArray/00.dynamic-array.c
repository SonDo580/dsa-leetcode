/* Dynamic Array implementation:
- limitation: only handle integers.
- overflow strategy: double the size when array is full.
- underflow strategy: cut the size in half when array shrinks to 1/4 full.
  - do not cut the size in half right when half-full to avoid "fluctuation"
*/

#include <stdlib.h>
#include <stdio.h>

typedef struct
{
    int size;
    int capacity;
    int *entries;
} DynamicArray;

#define INITIAL_CAPACITY 10

/* Helper to show alert and exit when memory allocation failed */
void require_successful_alloc(void *ptr)
{
    if (ptr == NULL)
    {
        printf("Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
}

DynamicArray *initialize()
{
    int capacity = INITIAL_CAPACITY;
    DynamicArray *array = malloc(sizeof(DynamicArray));
    require_successful_alloc(array);

    array->entries = malloc(capacity * sizeof(int));
    require_successful_alloc(array->entries);

    array->capacity = capacity;
    array->size = 0;
    return array;
}

void push(DynamicArray *array, int value)
{
    if (array->size == array->capacity)
    {
        array->capacity *= 2;
        array->entries = realloc(array->entries, array->capacity * sizeof(int));
        require_successful_alloc(array->entries);
    }
    array->entries[(array->size)++] = value;
}

int pop(DynamicArray *array)
{
    if (array->size == 0)
    {
        printf("Pop empty array\n");
        exit(EXIT_FAILURE);
    }

    int value = array->entries[--(array->size)];
    if (array->size == array->capacity / 4)
    {
        array->capacity /= 2;
        array->entries = realloc(array->entries, array->capacity * sizeof(int));
        require_successful_alloc(array->entries);
    }
    return value;
}

void free_array(DynamicArray *array)
{
    free(array->entries);
    free(array);
}

void print_array(DynamicArray *array)
{
    printf("size / capacity: %d / %d\nelements: ", array->size, array->capacity);
    for (int i = 0; i < array->size; i++)
        printf("%d ", array->entries[i]);
    printf("\n");
}

int main()
{
    DynamicArray *array = initialize();
    for (int i = 0; i < 2 * INITIAL_CAPACITY; i++)
        push(array, i);
    print_array(array);

    int size = array->size;
    for (int i = size; i > size / 5; i--)
        pop(array);
    print_array(array);

    free_array(array);
}
