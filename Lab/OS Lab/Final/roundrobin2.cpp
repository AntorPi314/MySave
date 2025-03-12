#include <bits/stdc++.h>
using namespace std;

struct Process {
    int id;          // Process ID
    int burstTime;   // Burst time of the process
    int remainingTime; // Remaining time to complete the process
};

void roundRobinScheduling(vector<Process>& processes, int timeQuantum) {
    queue<Process> readyQueue;
    vector<int> waitingTime(processes.size(), 0);
    vector<int> turnaroundTime(processes.size(), 0);
    vector<int> completionTime(processes.size(), 0); // Stores completion times of processes

    // Load all processes into the ready queue initially
    for (auto& process : processes) {
        readyQueue.push(process);
    }

    int currentTime = 0;

    while (!readyQueue.empty()) {
        Process currentProcess = readyQueue.front();
        readyQueue.pop();

        // Execute the process for the given time quantum or its remaining time, whichever is smaller
        int executionTime = min(currentProcess.remainingTime, timeQuantum);
        currentTime += executionTime;
        currentProcess.remainingTime -= executionTime;

        // If the process has remaining time, push it back into the queue
        if (currentProcess.remainingTime > 0) {
            readyQueue.push(currentProcess);
        } else {
            // Calculate turnaround time, waiting time, and completion time
            int processIndex = currentProcess.id - 1;
            turnaroundTime[processIndex] = currentTime;
            waitingTime[processIndex] = turnaroundTime[processIndex] - processes[processIndex].burstTime;
            completionTime[processIndex] = currentTime; // Completion time is the current time when the process finishes
        }
    }

    // Display results
    cout << "Process ID\tBurst Time\tWaiting Time\tTurnaround Time\tCompletion Time\n";
    for (int i = 0; i < processes.size(); ++i) {
        cout << processes[i].id << "\t\t"
             << processes[i].burstTime << "\t\t"
             << waitingTime[i] << "\t\t"
             << turnaroundTime[i] << "\t\t"
             << completionTime[i] << "\n";
    }
}

int main() {
    vector<Process> processes = {
        {1, 5, 5},
        {2, 3, 3},
        {3, 8, 8},
        {4, 6, 6}
    };

    int timeQuantum = 2;

    cout << "Round Robin CPU Scheduling (Time Quantum = " << timeQuantum << ")\n";
    roundRobinScheduling(processes, timeQuantum);

    return 0;
}
