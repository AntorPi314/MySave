#include <bits/stdc++.h>
using namespace std;

// Process structure to represent a process
struct process {
    int processID; // Unique identifier for a process
    process(int id) : processID(id) {}
};

// Counting semaphore structure
struct semaphore {
    int value; // The count of available resources
    queue<process> q; // Queue for blocked processes
    mutex mtx; // Mutex for thread-safe operations

    semaphore(int initialValue) : value(initialValue) {} // Initialize semaphore with a count
};

// Simulate blocking a process
void sleep() {
    cout << "Process is sleeping (blocked)." << endl;
}

// Simulate waking up a process
void wakeup(process p) {
    cout << "Waking up process with ID: " << p.processID << endl;
}

// P (Down/Wait) operation for counting semaphore
void P(semaphore &s, process &currentProcess) {
    unique_lock<mutex> lock(s.mtx); // Lock the semaphore for thread-safe access
    if (s.value > 0) { // If resources are available
        s.value--; // Decrease the count (resource acquired)
        cout << "Process " << currentProcess.processID << " acquired a resource. Remaining: " << s.value << endl;
    } else {
        // If no resources are available, block the process
        s.q.push(currentProcess);
        cout << "Process " << currentProcess.processID << " is blocked and added to the queue." << endl;
        sleep(); // Simulate process being blocked
    }
}

// V (Up/Signal) operation for counting semaphore
void V(semaphore &s) {
    unique_lock<mutex> lock(s.mtx); // Lock the semaphore for thread-safe access
    if (s.q.empty()) { // If no processes are waiting
        s.value++; // Increment the resource count
        cout << "A resource has been released. Available: " << s.value << endl;
    } else {
        // If processes are waiting, wake one up
        process p = s.q.front();
        s.q.pop(); // Remove the process from the queue
        wakeup(p); // Simulate waking up the process
    }
}

// Main function to demonstrate the counting semaphore
int main() {
    semaphore s(2); // Create a counting semaphore with 2 resources available

    // Create some processes
    process p1(1);
    process p2(2);
    process p3(3);
    process p4(4);

    // Simulate the P and V operations
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
