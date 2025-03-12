#include <bits/stdc++.h>
using namespace std;

struct process {
    int processID;
    process(int id) : processID(id) {}
};
struct semaphore {
    int value;
    queue<process> q;
    semaphore(int initialValue) : value(initialValue) {}
};

void sleep() {
    cout<<"Process is sleeping (blocked)"<<endl;
}

void wakeup(process p) {
    cout<<"Waking up process with ID: "<<p.processID<<endl;
}

void P(semaphore &s, process &currentProcess) {
    if (s.value == 1) {
        s.value = 0;
        cout<<"Process"<<currentProcess.processID<<"acquired the semaphore"<<endl;
    } else {
        s.q.push(currentProcess);
        cout<<"Process"<<currentProcess.processID<<"is blocked and added to the queue"<<endl;
        sleep();
    }
}

void V(semaphore &s) {
    if (s.q.empty()) {
        s.value = 1;
        cout<<"Semaphore is released and available"<<endl;
    } else {
        process p = s.q.front();
        s.q.pop();
        wakeup(p);
    }
}

int main() {
    semaphore s(1);
    process p1(1);
    process p2(2);
    process p3(3);
    cout<<"Process 1 tries to enter critical section"<<endl;
    P(s, p1); // Process 1 acquires the semaphore

    cout<<"Process 2 tries to enter critical section"<<endl;
    P(s, p2); // Process 2 is blocked

    cout<<"Process 3 tries to enter critical section"<<endl;
    P(s, p3); // Process 3 is blocked

    cout<<"Process 1 leaves the critical section."<<endl;
    V(s); // Process 2 is woken up

    cout<<"Process 2 leaves the critical section."<<endl;
    V(s); // Process 3 is woken up

    cout<<"Process 3 leaves the critical section."<<endl;
    V(s); // Semaphore is released and available
    return 0;
}
