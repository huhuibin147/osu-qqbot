#include <stdio.h>
#include<math.h>
#include "demo.h"


void wtmsb(double pp,int pc,int tth,double bp1,double bp5,double acc1,double acc2,double acc3) {
	double A1 = 0;
	double A2 = 0;
	double A31 = 0;
	double A3 = 0;
	double A4 = 0;
	double total = 0;
	if (pp*pc*tth*bp1*bp5*acc1*acc2*acc3 == 0) {
		printf("这号数据不正常\n");
	}
	else{
		A1 = pp/(4*bp1-3*bp5);
		A2 = log(tth/pc)/log(15.5);
		if (pp < 1000) A31 = 1000*pc/(1.2*pp)-400;
		else if (pp < 7000) A31 = 1000*pc/(0.0008*pp*pp+0.4*pp)-400;
		else A31 = 1000*pc/(6*pp)-400;
		if (A31 > 1) A3 = log(A31)/log(24.5);
		else A3 = 0;
		A4 = pow((acc1+acc2+acc3)/3,5);
		total = A1*A2*A3*A4;
		printf("BP指标:%.2f 参考值12.00\n",A1);
		printf("TTH指标:%.2f 参考值2.00\n",A2);
		printf("PC指标:%.2f 参考值2.00\n",A3);
		printf("ACC指标:%.4f 参考值0.9000\n",A4);
		printf("综合指标:%.2f\n",total);
		if (pp < 300) printf("该号pp较低，不作出评价\n");
		else if (total >= 55) printf("该号成绩卓越，同分段中的王者!\n");
		else if (total >= 44) printf("该号成绩优秀，标准的正常玩家!\n");
		else if (A3 < 1 || A1 < 3) printf("结论:基本断定是小号或者离线党!\n");
		else if (A3 < 1.7) {
			if (A1 < 9) printf("结论:要么天赋超群，要么小号或者离线党,总之这个pp严重虚低!\n");
			else{
				if (A4 < 0.75) printf("结论:虽然天赋超群,但是求你别糊图了!\n");
				else if (A4 < 0.88) printf("结论:虽然天赋超群，但是建议花些pc好好练习一下acc吧!\n");
				else if (A2 < 1.7) printf("结论:是一个有天赋的超级pp刷子,求求你不要re了!\n");
				else if (A2 < 1.9) printf("结论:是一个有天赋的高级pp刷子,建议降低re图次数!\n");
				else printf("结论:是一个有天赋又认真的pp刷子,建议多打点综合图!\n");
			}
		}
		else if (A3 < 1.9) {
			if (A1 < 9 && A4 > 0.75) printf("结论:有一定天赋，将来一定时间内还是可以飞升一波的!\n");
			if (A1 < 11 && A4 > 0.75) printf("结论:有一定天赋，将来一定时间内还是可以小幅涨一点的!\n");
			else{
				if (A4 < 0.75) printf("结论:虽然有一些天赋,但是求你别糊图了!\n");
				else if (A4 < 0.88) printf("结论:虽然有一些天赋，但是建议花些pc好好练习一下acc吧!\n");
				else if (A2 < 1.7) printf("结论:是一个标准pp刷子,求求你不要re了!\n");
				else if (A2 < 1.9) printf("结论:是一个标准pp刷子,建议降低re图次数!\n");
				else if (A2 < 2.1) printf("结论:是一个标准pp刷子,建议多打点综合图!\n");
				else printf("结论:这种情况比较罕见，你应该和各种类型的人都不一样!\n");
			}
		}
		else if (A3 < 2.1) {
			if (A1 < 9 && A4 > 0.75) printf("结论:看样子正渡过瓶颈期了，将来一定时间内还是可以飞升一波的!\n");
			if (A1 < 11 && A4 > 0.75) printf("结论:要么即将渡过瓶颈期，要么之前飞太快即将进入瓶颈期!\n");
			else{
				if (A4 < 0.75) printf("结论:你啥都不错,但是求你别糊图了!\n");
				else if (A4 < 0.88) printf("结论:比较正常，但是建议好好练习一下acc吧!\n");
				else if (A2 < 1.7) printf("结论:是一个没天赋的pp刷子,求求你不要re了!\n");
				else if (A2 < 1.9) printf("结论:是一个没天赋的pp刷子,建议降低re图次数!\n");
				else printf("结论:比较正常，但是可能某些方面有所欠缺，请参考指标!\n");
			}
		}
		else if (A3 < 2.4) {
			if (A1 < 9 && A4 > 0.75) printf("结论:相信自己，你正在飞升!\n");
			if (A1 < 11 && A4 > 0.75) printf("结论:也许在瓶颈期附近，但是相信你能克服它!\n");
			else{
				if (A4 < 0.75) printf("结论:你真的很强,但是求你别糊图了!\n");
				else if (A4 < 0.88) printf("结论:你真的很强，但是建议好好练习一下acc吧!\n");
				else if (A2 < 1.7) printf("结论:是一个没救了的pp刷子,求求你不要re了!\n");
				else if (A2 < 1.9) printf("结论:是一个没救了的pp刷子,建议降低re图次数!\n");
				else printf("结论:这孩子瓶颈了!\n");
			}
		}
		else {
			if (A1 < 10 && A4 > 0.75) printf("结论:打图经验充足，不飞升没理由!\n");
			else{
				if (A2 < 1.8) printf("结论:你这么个re图毫无用处，好好考虑下吧!\n");
				else printf("结论:你不适合屙屎，删游戏吧!\n");
			}
		}
	}
}




