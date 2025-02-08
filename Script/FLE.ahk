#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

str1 =
(

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


)

str2 =
(

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


)

str3 =
(

#include <bits/stdc++.h>
using namespace std;

int main() {
    int bt[20],p[20],wt[20],tat[20],pr[20],i,j,n,total=0,pos,temp,avg_wt,avg_tat;
    cout<<"Enter Total Number of Process:";
    cin>>n;
    cout<<"\nEnter Burst Time and Priority\n";
    for(i=0; i<n; i++) {
        cout<<"\nP["<<i+1<<"]\n";
        cout<<"Burst Time:";
        cin>>bt[i];
        cout<<"Priority:";
        cin>>pr[i];
        p[i]=i+1;           //contains process number
    }
    //sorting burst time, priority and process number in ascending order using selection sort
    for(i=0; i<n; i++) {
        pos=i;
        for(j=i+1; j<n; j++) {
            if(pr[j]<pr[pos])
                pos=j;
        }
        temp=pr[i];
        pr[i]=pr[pos];
        pr[pos]=temp;
        temp=bt[i];
        bt[i]=bt[pos];
        bt[pos]=temp;
        temp=p[i];
        p[i]=p[pos];
        p[pos]=temp;
    }
    wt[0]=0;            //waiting time for first process is zero
    //calculate waiting time
    for(i=1; i<n; i++) {
        wt[i]=0;
        for(j=0; j<i; j++)
            wt[i]+=bt[j];
        total+=wt[i];
    }
    avg_wt=total/n;      //average waiting time
    total=0;
    cout<<"\nProcess\t    Burst Time    \tWaiting Time\tTurnaround Time";
    for(i=0; i<n; i++) {
        tat[i]=bt[i]+wt[i];     //calculate turnaround time
        total+=tat[i];
        cout<<"\nP["<<p[i]<<"]\t\t  "<<bt[i]<<"\t\t    "<<wt[i]<<"\t\t\t"<<tat[i];
    }
    avg_tat=total/n;     //average turnaround time
    cout<<"\n\nAverage Waiting Time="<<avg_wt;
    cout<<"\nAverage Turnaround Time="<<avg_tat;
    return 0;
}


)

str4 =
(

#include <bits/stdc++.h>
using namespace std;

struct Process {
    int id;         // Process ID
    int burstTime;  // Burst time of the process
    int remainingTime; // Remaining time to complete the process
};

void roundRobinScheduling(vector<Process>& processes, int timeQuantum) {
    queue<Process> readyQueue;
    vector<int> waitingTime(processes.size(), 0);
    vector<int> turnaroundTime(processes.size(), 0);

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
            // Calculate turnaround time and waiting time
            int processIndex = currentProcess.id - 1;
            turnaroundTime[processIndex] = currentTime;
            waitingTime[processIndex] = turnaroundTime[processIndex] - processes[processIndex].burstTime;
        }
    }

    // Display results
    cout << "Process ID\tBurst Time\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < processes.size(); ++i) {
        cout << processes[i].id << "\t\t"
             << processes[i].burstTime << "\t\t"
             << waitingTime[i] << "\t\t"
             << turnaroundTime[i] << "\n";
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


)

str5 =
(

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


)

str6 =
(


#include <bits/stdc++.h>
using namespace std;

int main() {
    int i,n,time,remain,temps=0,time_quantum;
    int wt=0,tat=0;
    cout<<"Enter the total number of process="<<endl;
    cin>>n;
    remain=n;
    // assigning the number of process to remain variable
    int at[n];
    int bt[n];
    int rt[n];
    cout<<"Enter the Arrival time, Burst time for All the processes"<<endl;
    for(i=0; i<n; i++) {
        cout<<"Arrival time for process "<<i+1<<endl;
        cin>>at[i];
        cout<<"Burst time for process "<<i+1<<endl;
        cin>>bt[i];
        rt[i]=bt[i];
    }
    cout<<"Enter the value of time QUANTUM:"<<endl;
    cin>>time_quantum;
    cout<<"\n\nProcess\t:Turnaround Time:Waiting Time\n\n";
    for(time=0,i=0; remain!=0;) {
        if(rt[i]<=time_quantum && rt[i]>0) {
            time += rt[i];
            rt[i]=0;
            temps=1;
        }

        else if(rt[i]>0) {
            rt[i] -= time_quantum;
            time += time_quantum;
        }

        if(rt[i]==0 && temps==1) {
            remain--;
            //Displaying the result of wating, turn around time:
			printf("Process { d}\t:\t d\t:\t d\n", i + 1, time - at[i], time - at[i] - bt[i]);
            cout<<endl;
            wt += time-at[i]-bt[i];
            tat += time-at[i];
            temps=0;
        }
        if(i == n-1)
            i=0;
        else if(at[i+1] <= time)
            i++;
        else
            i=0;
    }
    cout<<"Average waiting time "<<wt*1.0/n<<endl;
    cout<<"Average turn around time "<<tat*1.0/n<<endl;
    return 0;
}



)

str7 =
(

#include <bits/stdc++.h>
using namespace std;

struct Process {
    int pid; // Process ID
    int bt; // Burst Time
    int art; // Arrival Time
};


void findWaitingTime(Process proc[], int n,
                     int wt[]) {
    int rt[n];

    // Copy the burst time into rt[]
    for (int i = 0; i < n; i++)
        rt[i] = proc[i].bt;

    int complete = 0, t = 0, minm = INT_MAX;
    int shortest = 0, finish_time;
    bool check = false;

    // Process until all processes gets
    // completed
    while (complete != n) {


        for (int j = 0; j < n; j++) {
            if ((proc[j].art <= t) &&
                    (rt[j] < minm) && rt[j] > 0) {
                minm = rt[j];
                shortest = j;
                check = true;
            }
        }

        if (check == false) {
            t++;
            continue;
        }

        // Reduce remaining time by one
        rt[shortest]--;

        // Update minimum
        minm = rt[shortest];
        if (minm == 0)
            minm = INT_MAX;

        // If a process gets completely
        // executed
        if (rt[shortest] == 0) {

            // Increment complete
            complete++;
            check = false;

            // Find finish time of current
            // process
            finish_time = t + 1;

            // Calculate waiting time
            wt[shortest] = finish_time -
                           proc[shortest].bt -
                           proc[shortest].art;

            if (wt[shortest] < 0)
                wt[shortest] = 0;
        }
        // Increment time
        t++;
    }
}

// Function to calculate turn around time
void findTurnAroundTime(Process proc[], int n,
                        int wt[], int tat[]) {
    // calculating turnaround time by adding
    // bt[i] + wt[i]
    for (int i = 0; i < n; i++)
        tat[i] = proc[i].bt + wt[i];
}

// Function to calculate average time
void findavgTime(Process proc[], int n) {
    int wt[n], tat[n], total_wt = 0,
                       total_tat = 0;

    // Function to find waiting time of all
    // processes
    findWaitingTime(proc, n, wt);


    findTurnAroundTime(proc, n, wt, tat);


    cout << " P\t\t"
         << "BT\t\t"
         << "WT\t\t"
         << "TAT\t\t\n";


    for (int i = 0; i < n; i++) {
        total_wt = total_wt + wt[i];
        total_tat = total_tat + tat[i];
        cout << " " << proc[i].pid << "\t\t"
             << proc[i].bt << "\t\t " << wt[i]
             << "\t\t " << tat[i] << endl;
    }

    cout << "\nAverage waiting time = "
         << (float)total_wt / (float)n;
    cout << "\nAverage turn around time = "
         << (float)total_tat / (float)n;
}

// Driver code
int main() {
    Process proc[] = { { 1, 6, 2 }, { 2, 2, 5 },
        { 3, 8, 1 }, { 4, 3, 0}, {5, 4, 4}
    };
    int n = sizeof(proc) / sizeof(proc[0]);

    findavgTime(proc, n);
    return 0;
}



)

str8 =
(



)

!1::
    Clipboard := str1
return

!2::
    Clipboard := str2
return

!3::
    Clipboard := str3
return

!4::
    Clipboard := str4
return

!5::
    Clipboard := str5
return

!6::
    Clipboard := str6
return

!7::
    Clipboard := str7
return

!8::
    Clipboard := str8
return

!0::
    Clipboard := ""
return