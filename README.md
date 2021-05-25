# Mobius Evaluation Code

This repository contains scripts to run most of the experiments using [Mobius](https://github.com/mobius-scheduler/mobius) from our [Mobisys paper](https://web.mit.edu/arjunvb/pubs/mobius-mobisys21-paper.pdf). This README explains how to setup the evaluation environment and run the experiments.

## Quick Start
* [Required Setup](#required-setup)
* [Installation](#installation)
* [Running Experiments](#reproducible-experiments)

## Required Setup
You should be able to run most the experiments on any machine running Ubuntu or MacOS. We ran our experiments on an Amazon EC2 `t2.xlarge` instance with 4 CPUs running Ubuntu 18.04. The Mobius implementation is multi-threaded, so for good performance, we recommend a machine with multiple CPUs. We provide instructions below for Ubuntu.

## Installation
Follow these steps to install Mobius and dependencies for the experiment instrumentation and plotting scripts:
1. Install [Go](https://golang.org/doc/install) (to run Mobius):
    ```
    wget -c https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz -O - | sudo tar -xz -C /usr/local
    ```
    
2. Add `export PATH=$PATH:/usr/local/go/bin` to your .bashrc and source (`source ~/.bashrc`).

3. Install python3 and R:
    ```
    sudo apt-get update
    sudo apt-get install -y python3.6 r-base python3-pip
    ```

4. Clone this repository:
    ```
    git clone --recurse-submodules https://github.com/mobius-scheduler/evaluation
    cd evaluation/
    ```

5. Install dependencies:
    ```
    pip3 install -r requirements.txt
    sudo Rscript requirements.r
    ```

## Reproducible Experiments
We provide scripts to reproduce **Figures 4d, 8, and 15-17**. Scripts to run the experiments for Figures 10-12 are also included (`lyft.py`, `exps/lyft/lyft.cfg`); however, these experiments take ~12 hours and require a server with 36 CPUs (in order to parallelize Mobius) and 72 GB of memory (in order to buffer all of the ridesharing requests). If you would like to learn more about running these Lyft ridesharing experiments, please get in touch.

Each script runs Mobius with the relevant parameters, parses the logs, generates the plots, and saves them as PDFs. Each script takes as input the path to a config file for each experiment. You can navigate through the `exps` folder to see the config files and the input data for the trace-driven emulation. Below, we tabulate the scripts to run the experiments, the paths to the plots, and the expected output from each plot. Each script below should take less than 30 minutes to execute the trace-driven emulation and generate the plots.

### Figure 4d (Dynamic convex boundaries)
| Info            |  Details                               |
| :----:          | :----                                |
| Script          | `python3 boundary.py exps/boundary/boundary.cfg` |
| Plot            | `data/boundary/boundary.pdf`                   |
| Expected output | - tight band of convex boundaries (width approximately 10 tasks/round)<br>- average target throughput should lie near Mobius throughput |

### Figure 8 (Mobius for different alphas)
| Info            |  Details                                        |
| :----:          | :----                                         |
| Script          | `python3 dynamic.py exps/dynamic/dynamic.cfg` |
| Plot            | `data/dynamic/dynamic.pdf`                      |
| Expected output | - max throughput should starve customer 2<br>- round-robin should give equal throughputs, but very low total throughput<br>- dedicating vehicles should give more throughput to customer 1<br>- customer throughputs should become more equal as alpha increases |

### Figures 15-16 (Aerial sensing case study)
| Info            |  Details                                                        |
| :----:          | :----                                                         |
| Script          | `python3 aerial.py exps/aerial/aerial.cfg`                    |
| Plots           | `data/aerial/aerial-thp.pdf`<br>`data/aerial/aerial-completion.pdf` |
| Expected output<br>Figure 15 | - "dedicated drones" should have roughly equal slices of the total throughput<br>- "max throughput" should give the largest share of throughput to the iPerf app<br>- "max throughput" should gradually ramp up its throughput for the Air Quality app<br>- "Mobius (prop. fair)" should give less throughput to iPerf than "max throughput"<br>- "Mobius (prop. fair)" should give more throughput to the Air Quality app than "max throughput"<br>- "Mobius (max-min)" should give a more even share of throughput across the apps than "max throughput"<br>- "Mobius (max-min)" should give more total throughput than "dedicated drones" |
| Expected output<br>Figure 16 | - "dedicated drones" should complete a high percentage (> 75%) of Parking and Traffic tasks<br> - "dedicated drones" should complete a low percentage (< 30%) of iPerf, Air Quality, and Roof tasks<br>- "Mobius (max-min)" should complete a greater percentage of Roof, Traffic, and Parking tasks than "max throughput" does<br>- "Max throughput" should complete a greater percentage of iPerf and Air Quality tasks than "Mobius (max-min)" does<br> - "Mobius (prop. fair)" should fulfill a greater percentage of iPerf and Air Quality tasks than does "Mobius (max-min)"|

### Figure 17 (Discount factor)
| Info            |  Details                                                        |
| :----:          | :----                                                         |
| Script          | `python3 discount.py exps/discount/discount.cfg`              |
| Plot            | `data/discount/discount.pdf`                                    |
| Expected output | - "no discount" should have one high peak (nearly 40 tasks)<br>- tasks fulfilled by "discount" should be more spread out over time<br>- "discount" should have multiple peaks with half the magnitude |
