#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Runtime v1.0.1 (Integer Patch)
void print_num(long long n) { printf("%lld\n", n); }
void print_str(char* s) { printf("%s\n", s); }

long long clock_ms() {
    return (long long)((double)clock() / CLOCKS_PER_SEC * 1000.0);
}

char* file_read(char* path) {
    FILE* f = fopen(path, "rb");
    if(!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = malloc(len + 1);
    fread(buf, 1, len, f);
    buf[len] = 0;
    fclose(f);
    return buf;
}

void file_write_bytes(char* path, void* list) {
    FILE* f = fopen(path, "wb");
    if(!f) return;
    // List logic stub for v1.0.1
    fclose(f);
}

void fill(void* list, void* count) {
    // Stub
}

// Array/List Stub
typedef struct {
    int capacity;
    int length;
    void** items;
} List;

List* new_list() {
    List* l = malloc(sizeof(List));
    l->capacity = 16;
    l->length = 0;
    l->items = malloc(sizeof(void*) * 16);
    return l;
}

void push(List* l, void* item) {
    if(l->length >= l->capacity) {
        l->capacity *= 2;
        l->items = realloc(l->items, sizeof(void*) * l->capacity);
    }
    l->items[l->length++] = item;
}

int len(void* obj) {
    return ((List*)obj)->length; 
}

// Simple Hash Map
typedef struct {
    char* key;
    void* value;
} Entry;

typedef struct {
    int capacity;
    int count;
    Entry* entries;
} Map;

Map* new_map() {
    Map* m = malloc(sizeof(Map));
    m->capacity = 16;
    m->count = 0;
    m->entries = calloc(16, sizeof(Entry));
    return m;
}

void map_set(Map* m, char* key, void* val) {
    for(int i=0; i<m->count; i++) {
        if(strcmp(m->entries[i].key, key) == 0) {
            m->entries[i].value = val;
            return;
        }
    }
    if(m->count >= m->capacity) return; 
    m->entries[m->count].key = key;
    m->entries[m->count].value = val;
    m->count++;
}

void* map_get(Map* m, char* key) {
    for(int i=0; i<m->count; i++) {
        if(strcmp(m->entries[i].key, key) == 0) return m->entries[i].value;
    }
    return NULL;
}

// Mock get_args
List* get_args() {
    List* l = new_list();
    return l;
}

int main(int argc, char** argv) {
print_str("Starting Memory Benchmark...");
long long start = clock_ms();
for(long long _i = 0; _i < 1000000; _i++) {
	long long a = ({ List* l = new_list(); push(l, (void*)1); push(l, (void*)2); push(l, (void*)3); push(l, (void*)4); push(l, (void*)5); l; });
}
long long end = clock_ms();
print_str("Done.");
print_str("Time (ms):");
print_num((end - start));
	return 0;
}