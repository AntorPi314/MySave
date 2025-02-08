#include <bits/stdc++.h>
using namespace std;

struct process {
    int processID;
    process(int id) : processID(id) {}
};
struct semaphore {
    int value;
    queue<process> q;
    mutex mtx; // Mutex for thread-safe operations
    semaphore(int initialValue) : value(initialValue) {}
};

void sleep() {
    cout << "Process is sleeping (blocked)" << endl;
}

void wakeup(process p) {
    cout << "Waking up process with ID: " << p.processID << endl;
}

void P(semaphore &s, process &currentProcess) {
    unique_lock<mutex> lock(s.mtx); // Lock the semaphore for thread-safe access
    if (s.value > 0) {
        s.value--;
        cout << "Process " << currentProcess.processID << " acquired a resource. Remaining: " << s.value << endl;
    } else {
        s.q.push(currentProcess);
        cout << "Process " << currentProcess.processID << " is blocked and added to the queue" << endl;
        sleep();
    }
}

void V(semaphore &s) {
    unique_lock<mutex> lock(s.mtx); // Lock the semaphore for thread-safe access
    if (s.q.empty()) {
        s.value++;
        cout << "A resource has been released. Available: " << s.value << endl;
    } else {
        process p = s.q.front();
        s.q.pop();
        wakeup(p);
    }
}

int main() {
    semaphore s(2); // Create a counting semaphore with 2 resources available

    process p1(1);
    process p2(2);
    process p3(3);
    process p4(4);

    cout << "Process 1 tries to acquire a resource." << endl;
    P(s, p1); // Process 1 acquires a resource

    cout << "Process 2 tries to acquire a resource." << endl;
    P(s, p2); // Process 2 acquires a resource

    cout << "Process 3 tries to acquire a resource." << endl;
    P(s, p3); // Process 3 is blocked

    cout << "Process 4 tries to acquire a resource." << endl;
    P(s, p4); // Process 4 is blocked

    cout << "Process 1 releases a resource." << endl;
    V(s); // Process 3 is woken up

    cout << "Process 2 releases a resource." << endl;
    V(s); // Process 4 is woken up

    cout << "Process 3 releases a resource." << endl;
    V(s); // Resource is now available
    return 0;
}
