/*
 * ctrl_temp.c
 *
 * Created: 08/11/2018 20:06:44
 * Author : sergi
 */ 

#define F_CPU 16000000 /* Define CPU Frequency 16MHz */
#define BAUD 9600 // BAUD RATE
#define MYUBRR F_CPU/16/BAUD-1 //UBRR

#include <avr/io.h> // Internal Includes
#include <avr/interrupt.h> // Interrupt Includes			
#include <stdio.h> 
#include <stdlib.h>
#include <util/delay.h>

#include "USART_irq.h" 

static FILE mystdout = FDEV_SETUP_STREAM(USART0_Transmit_IO,NULL,_FDEV_SETUP_WRITE);  

void adc_init(void)
{
	ADMUX = (1<<REFS0);     //select AVCC as reference
	ADCSRA = (1<<ADEN) | 7;  //enable and prescale = 128 (16MHz/128 = 125kHz)
}

int readAdc(char chan)
{
	ADMUX = (1<<REFS0) | (chan & 0x0f);  //select input and ref
	ADCSRA |= (1<<ADSC);                 //start the conversion
	while (ADCSRA & (1<<ADSC));          //wait for end of conversion
	return ADCW;
}
int main(void)
{
	USART0_Init(MYUBRR); /* Initialize USART */
	adc_init();		/* Initialize the ADC */
	char array[10];  //declarations
	int ADC_value;
	char chan = 0; 
	float temp;
	int accum = 0;
	int i; 
	sei(); //service enable interrupts
	stdout = &mystdout; 
    while (1) 
    {	
		for (i=0;i<5;i++){
			ADC_value= readAdc(chan); //reading
			accum += ADC_value;
			_delay_ms(100);
		} 
		
		temp = ((accum*4.88/5)-0.0027)/10;
		printf("%s\n",itoa((int)temp,array,10));
		accum =0; 
	}
}


