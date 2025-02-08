#include <bits/stdc++.h>
using namespace std;

// Simulating a process structure
struct process {
    int processID; // Unique identifier for the process
    process(int id) : processID(id) {}
};

// Semaphore structure
struct semaphore {
    int value; // 0 for unavailable, 1 for available
    queue<process> q; // Queue for blocked processes

    // Constructor to initialize the semaphore
    semaphore(int initialValue) : value(initialValue) {}
};

// Simulate blocking a process
void sleep() {
    cout << "Process is sleeping (blocked)." << endl;
}

// Simulate waking up a process
void wakeup(process p) {
    cout << "Waking up process with ID: " << p.processID << endl;
}

// Down/Wait operation
void P(semaphore &s, process &currentProcess) {
    if (s.value == 1) {
        s.value = 0; // Acquire the semaphore
        cout << "Process " << currentProcess.processID << " acquired the semaphore." << endl;
    } else {
        // Add the process to the waiting queue and block it
        s.q.push(currentProcess);
        cout << "Process " << currentProcess.processID << " is blocked and added to the queue." << endl;
        sleep();
    }
}

// Up/Signal operation
void V(semaphore &s) {
    if (s.q.empty()) {
        s.value = 1; // Release the semaphore
        cout << "Semaphore is released and available." << endl;
    } else {
        // Select a process from the waiting queue
        process p = s.q.front();
        s.q.pop(); // Remove the process from the waiting queue
        wakeup(p); // Wake up the process
    }
}

// Main function to demonstrate the functionality
int main() {
    // Create a semaphore with an initial value of 1 (available)
    semaphore s(1);

    // Create some processes
    process p1(1);
    process p2(2);
    process p3(3);

    // Simulate the P and V operations
    cout << "Process 1 tries to enter critical section." << endl;
    P(s, p1); // Process 1 acquires the semaphore

    cout << "Process 2 tries to enter critical section." << endl;
    P(s, p2); // Process 2 is blocked

    cout << "Process 3 tries to enter critical section." << endl;
    P(s, p3); // Process 3 is blocked

    cout << "Process 1 leaves the critical section." << endl;
    V(s); // Process 2 is woken up

    cout << "Process 2 leaves the critical section." << endl;
    V(s); // Process 3 is woken up

    cout << "Process 3 leaves the critical section." << endl;
    V(s); // Semaphore is released and available
    return 0;
}
