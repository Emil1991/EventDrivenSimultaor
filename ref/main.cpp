/*
 * network.cpp
 *
 *  Created on: Dec 12, 2018
 *      Author: shmooz
 */

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <random>
#include <vector>
#include <math.h>
#include <ctime>
//#include <chrono>
#include <functional>
using namespace std;

class InPort
{
public:
	double num_of_packages_in_ts;
	vector<double> prob;
	double chosen_pack;
	double current_sent_pack;

	InPort()
	{
		num_of_packages_in_ts = 0;
		chosen_pack = 0;
		current_sent_pack = 0;
	}
	~InPort() = default;
};

class Input
{
public:
	int N;
	InPort* ports;

	Input(int n)
	{
		N = n;
		ports = new InPort[n];
	}
	~Input()
	{
		delete[] ports;
	}
};

class OutPort
{
public:
	unsigned int length;
	bool waiting_from_input;
	double rate;
	double current_length;
	double current_passed;
	double curr_service_time;
	vector<double> waiting_time;
	vector<bool> waiting_now;
	double chosen_rate;

	OutPort()
	{
		length = 0;
		waiting_from_input = false;
		current_length = 0;
		rate = 0;
		current_passed = 0;
		curr_service_time = 0;
		chosen_rate = 0;
	}
	~OutPort() = default;
};

class Output
{
public:
	int M;
	OutPort* ports;

	Output(int m)
	{
		M = m;
		ports = new OutPort[m];
	}
	~Output()
	{
		delete[] ports;
	}
};


int main(int argc, char** argv)
{
	double tim = atof(argv[1]);
	Input input(atoi(argv[2]));
	Output output(atoi(argv[3]));

	int i_success[output.M];
	for (int i = 0; i < output.M; i++)
		i_success[i] = 0;
	int success = 0;
	int i_fail[output.M];
	for (int i = 0; i < output.M; i++)
		i_fail[i] = 0;
	int fail = 0;
	double end_tim = tim;
	double wait_time_avg = 0;
	//double service_time_avg = 0;

	for (int i = 0; i < input.N; i++)
	{
		for (int j = 0; j < output.M; j++)
		{
			input.ports[i].prob.push_back(atof(argv[4 + j + output.M * i]));
		}
	}

	for (int i = 0; i < input.N; i++)
	{
		input.ports[i].num_of_packages_in_ts = atof(argv[4 + output.M * input.N + i]);
	}

	for (int i = 0; i < output.M; i++)
	{
		output.ports[i].length = atoi(argv[4 + output.M * input.N + input.N + i]);
		output.ports[i].rate = atof(argv[4 + output.M * input.N + i + input.N + output.M]);
	}

	bool is_waiting = false;
	bool next_ts = true;
	double max_service_time = 0;
	double service_time = 0;
	/*std::random_device rd;
	std::mt19937 gen(rd());
	std::mt19937 out_gen(rd());
	std::mt19937 in_gen(rd());
	std::mt19937 out_gen1(rd());
	std::mt19937 in_gen1(rd());
	std::mt19937 in_out_gen(rd());(*/
	//unsigned in_out_seed = std::chrono::system_clock::now().time_since_epoch().count();
	default_random_engine in_out_gen;//(in_out_seed);
	default_random_engine gen;//(in_out_seed);
	default_random_engine out_gen;//(in_out_seed);
	default_random_engine in_gen;//(in_out_seed);
	default_random_engine out_gen1;//(in_out_seed);
	default_random_engine in_gen1;//(in_out_seed);
	//int place = 0;
	while (tim > 0)
	{
		is_waiting = false;
		if (next_ts == true)
		{
			for (int i = 0; i < output.M; i++)
			{
				//unsigned out_seed = std::chrono::system_clock::now().time_since_epoch().count();
				//default_random_engine out_gen1(out_seed);
				std::poisson_distribution<> d_out1(output.ports[i].rate);
				output.ports[i].chosen_rate = d_out1(out_gen1);
			}
			
			for (int i = 0; i < input.N; i++)
			{	
				//unsigned in_seed = std::chrono::system_clock::now().time_since_epoch().count();
				//default_random_engine in_gen1(in_seed);
				std::poisson_distribution<> d_in1(input.ports[i].num_of_packages_in_ts);
				input.ports[i].chosen_pack = d_in1(in_gen1);
			}
			
			for (int i = 0; i < output.M; i++)
			{
				if (output.ports[i].waiting_from_input == false)
				{
					if ((output.ports[i].chosen_rate > output.ports[i].current_passed) && (output.ports[i].waiting_time.size() > 0))
					{
						if (output.ports[i].waiting_now.back() == true)
							wait_time_avg += abs(output.ports[i].waiting_time.back() - output.ports[i].current_passed/output.ports[i].chosen_rate);
						else				
							wait_time_avg += output.ports[i].waiting_time.back() + output.ports[i].current_passed/output.ports[i].chosen_rate;
						output.ports[i].waiting_time.pop_back();
						output.ports[i].waiting_now.pop_back();
						output.ports[i].waiting_from_input = true;
					}
				}
			}
		}
		//unsigned in_out_seed = std::chrono::system_clock::now().time_since_epoch().count();
		//default_random_engine in_out_gen(in_out_seed);
		/*std::uniform_int_distribution<> d_in_out(0,output.M + input.N - 1);*/
		//std::uniform_int_distribution<> d_in_out(0,output.M + input.N - 1);
		//int place = d_in_out(in_out_gen);
		std::uniform_int_distribution<> d_in_out(0,output.M + input.N - 1);
		int place = d_in_out(in_out_gen);
			
		if (place <= output.M - 1)
		{
			std::uniform_int_distribution<> d_out(0,output.M - 1);
			int out_place = d_out(out_gen);
			//int out_place = place;
			if ((output.ports[out_place].waiting_from_input == true) && (output.ports[out_place].chosen_rate > output.ports[out_place].current_passed))
			{
				service_time += 1;
				output.ports[out_place].current_passed += 1;
				if (tim <= 1)
					output.ports[out_place].curr_service_time += 1/output.ports[out_place].chosen_rate;	
				output.ports[out_place].waiting_from_input = false;
				if ((output.ports[out_place].chosen_rate > output.ports[out_place].current_passed) && (output.ports[out_place].waiting_time.size() > 0))
				{
					if (output.ports[out_place].waiting_now.back() == true)
					{
						wait_time_avg += abs(output.ports[out_place].waiting_time.back() - output.ports[out_place].current_passed/output.ports[out_place].chosen_rate);
					}
					else				
						wait_time_avg += output.ports[out_place].waiting_time.back() + output.ports[out_place].current_passed/output.ports[out_place].chosen_rate;
					output.ports[out_place].waiting_time.pop_back();
					output.ports[out_place].waiting_now.pop_back();
					output.ports[out_place].waiting_from_input = true;
				}
			}
			else
			{
				/*if ((output.ports[out_place].chosen_rate > output.ports[out_place].current_passed) && (output.ports[out_place].waiting_time.size() > 0))
				{
					cout << "kk";
					service_time += 1;
					//service_time_avg += 1/output.ports[out_place].chosen_rate;
					if (tim <= 1)
						output.ports[out_place].curr_service_time += 1/output.ports[out_place].chosen_rate;	
					if (output.ports[out_place].waiting_now.back() == true)
					{
						wait_time_avg += abs(output.ports[out_place].waiting_time.back() - output.ports[out_place].current_passed/output.ports[out_place].chosen_rate);
					}
					else				
						wait_time_avg += output.ports[out_place].waiting_time.back() + output.ports[out_place].current_passed/output.ports[out_place].chosen_rate;
					output.ports[out_place].waiting_time.pop_back();
					output.ports[out_place].waiting_now.pop_back();
					output.ports[out_place].current_passed += 1;
					if ((output.ports[out_place].chosen_rate > output.ports[out_place].current_passed) && (output.ports[out_place].waiting_time.size() > 0))
					{
						if (output.ports[out_place].waiting_now.back() == true)
						{
							wait_time_avg += abs(output.ports[out_place].waiting_time.back() - output.ports[out_place].current_passed/output.ports[out_place].chosen_rate);
						}
						else				
							wait_time_avg += output.ports[out_place].waiting_time.back() + output.ports[out_place].current_passed/output.ports[out_place].chosen_rate;
						output.ports[out_place].waiting_time.pop_back();
						output.ports[out_place].waiting_now.pop_back();
						output.ports[out_place].waiting_from_input = true;
					}	
				}*/
			}
		}			
		else
		{
			std::uniform_int_distribution<> d_in(0,input.N - 1);
			int in_place = place - output.M;

			if (input.ports[in_place].current_sent_pack < input.ports[in_place].chosen_pack)
			{
				discrete_distribution<> discrete(input.ports[in_place].prob.begin(),input.ports[in_place].prob.end());
				int chosen_out = discrete(gen);
				vector<double>::iterator it = output.ports[chosen_out].waiting_time.begin();
				vector<bool>::iterator it_bool = output.ports[chosen_out].waiting_now.begin();

				if (output.ports[chosen_out].current_passed == output.ports[chosen_out].chosen_rate)
				{
					if (output.ports[chosen_out].waiting_time.size() == output.ports[chosen_out].length) 
					{
						i_fail[chosen_out] += 1;
						fail += 1;
					}
					else
					{
						i_success[chosen_out] += 1;
						success += 1;
						output.ports[chosen_out].waiting_time.insert(it, (input.ports[in_place].chosen_pack - input.ports[in_place].current_sent_pack)/input.ports[in_place].chosen_pack);
						output.ports[chosen_out].waiting_now.insert(it_bool, true);
					}					
				}
				else 
				{
					if (output.ports[chosen_out].waiting_from_input == false) //&& (output.ports[chosen_out].waiting_time.size() == 0))
					{
						i_success[chosen_out] += 1;
						success += 1;
						output.ports[chosen_out].waiting_from_input = true;
					}
					else 
					{
						if (output.ports[chosen_out].waiting_time.size() == output.ports[chosen_out].length)
						{
							i_fail[chosen_out] += 1;
							fail += 1;
							//cout << "cdc";
						}
						else
						{
							i_success[chosen_out] += 1;
							success += 1;
							//if (output.ports[chosen_out].waiting_from_input == true)
							//{
							output.ports[chosen_out].waiting_time.insert(it, (input.ports[in_place].chosen_pack - input.ports[in_place].current_sent_pack)/input.ports[in_place].chosen_pack);
							output.ports[chosen_out].waiting_now.insert(it_bool, true);
							//}
							/*else
							{
								output.ports[chosen_out].waiting_from_input = true;
								cout << "dfh";
							}*/
						}	
					}
				}
				//else{cout << "fsfs";}
				input.ports[in_place].current_sent_pack += 1;
			}
		}
			//else{cout << "wsw";}
			//cout << input.ports[in_place].current_sent_pack<< ' ';
		//}
		
		//place ^= 1;
		for (int i = 0; i < output.M; i++)
		{
			if ((output.ports[i].current_passed < output.ports[i].chosen_rate) && (output.ports[i].waiting_time.size() != 0))
			{
				next_ts = false;
				break;
			}
			if ((output.ports[i].current_passed < output.ports[i].chosen_rate) && (output.ports[i].waiting_from_input == true))
			{
				next_ts = false;
				break;
			}
			next_ts = true;
		}
		if (next_ts == true)
		{
			for (int i = 0; i < input.N; i++)
			{
				if (input.ports[i].current_sent_pack < input.ports[i].chosen_pack)
				{
					next_ts = false;
					break;
				} 
				next_ts = true;
			}
		}
		if ((tim <= 1) && (next_ts == true))
		{
			for (int i = 0; i < output.M; i++)
			{
				if (output.ports[i].waiting_time.size() != 0)
				{
					is_waiting = true;
					break;
				}
			}
		}
		
		if (next_ts == true)
		{
			tim -= 1;
			for (int i = 0; i < output.M; i++)
			{
				//if (output.ports[i].current_passed > 0)
					//service_time_avg += 1/output.ports[i].current_passed;
				output.ports[i].current_passed = 0;

				for (unsigned int j = 0; j < output.ports[i].waiting_now.size(); j++)
				{
					if (output.ports[i].waiting_now[j] == false)
						output.ports[i].waiting_time[j] += 1;
					else
						output.ports[i].waiting_now[j] = false;
				}
			}
			for (int i = 0; i < input.N; i++)
			{
				input.ports[i].current_sent_pack = 0;
			}
			//if (service_time > 0)
				//service_time_avg += 1 / */service_time;//);
			//service_time = 0;
		}
				
		if (tim == 0) 
		{
			for (int i = 0; i < output.M; i++)
			{
				if ((output.ports[i].curr_service_time > max_service_time) && (is_waiting == false))
				{
					max_service_time = output.ports[i].curr_service_time;
				}
				if (is_waiting == true)
				{
					output.ports[i].curr_service_time = 0;
				}
			}
		}
	}

	if (max_service_time > 0)
			end_tim -= (1 - max_service_time); 

	double new_tim = 0;
	max_service_time = 0;
	while (is_waiting == true)
	{
		is_waiting = false;
		for (int i = 0; i < output.M; i++)
		{
			//unsigned out_seed = std::chrono::system_clock::now().time_since_epoch().count();
			//default_random_engine out_gen(out_seed);
			std::random_device rd;
			std::mt19937 out_gen(rd());
			std::poisson_distribution<> d_out(output.ports[i].rate);
			output.ports[i].chosen_rate = d_out(out_gen);

			if (output.ports[i].waiting_time.size() == 0)
			{
				continue;
			}

			if (output.ports[i].chosen_rate >= output.ports[i].waiting_time.size())
			{
				while (output.ports[i].waiting_time.size() > 0)
				{
					wait_time_avg += output.ports[i].waiting_time.back() + output.ports[i].current_passed/output.ports[i].chosen_rate;
					service_time += 1;
					//service_time_avg += 1/output.ports[i].chosen_rate;
					output.ports[i].curr_service_time += 1/output.ports[i].chosen_rate;
					output.ports[i].current_passed += 1;
					output.ports[i].waiting_time.pop_back();
				}
				continue;
			}

			if (output.ports[i].chosen_rate - output.ports[i].waiting_time.size() < 0)
			{
				for (int j = 0; j < output.ports[i].chosen_rate; j++)
				{
					wait_time_avg += output.ports[i].waiting_time.back() + output.ports[i].current_passed/output.ports[i].chosen_rate;
					service_time += 1;
					//service_time_avg += 1/output.ports[i].chosen_rate;
					output.ports[i].current_passed += 1;
					output.ports[i].curr_service_time += 1/output.ports[i].chosen_rate;
					output.ports[i].waiting_time.pop_back();
				}
				is_waiting = true;
			}
		}

		if (is_waiting == true)
		{
			for (int i = 0; i < output.M; i++)
			{
				//if (output.ports[i].current_passed > 0)
				//	service_time_avg += 1/output.ports[i].current_passed;
				output.ports[i].current_passed = 0;
				output.ports[i].curr_service_time = 0;
				for (unsigned int j = 0; j < output.ports[i].waiting_time.size(); j++)
				{
					output.ports[i].waiting_time[j] += 1;
				}
			}
			//if (service_time > 0)
				//service_time_avg += (1 / */service_time;//);
			//service_time = 0;
		}
		else
		{
			for (int i = 0; i < output.M; i++)
			{
				if (output.ports[i].curr_service_time > max_service_time)
				{
					max_service_time = output.ports[i].curr_service_time;
				}
			}
			//if (service_time > 0)
				//service_time_avg += /*(1 / */service_time;//);
			new_tim +=  max_service_time;
			break;
		}
		new_tim += 1;
	}

	end_tim += new_tim;
	cout << success << " ";
	for (int i = 0; i < output.M; i++)
	{
		cout << i_success[i] << " ";
	}
	cout << fail << " ";
	for (int i = 0; i < output.M; i++)
	{
		cout << i_fail[i] << " ";
	}

	cout << end_tim << " ";
	cout << end_tim/ wait_time_avg  << " ";
	cout << end_tim/ service_time << endl;
	return 0;
}
