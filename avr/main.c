/*
 * ctrl_temp.c
 *
 * Created: 08/11/2018 20:06:44
 * Author : sergi
 */ 

#define F_CPU 16000000 /* Define CPU Frequency e.g. here 16MHz */
#define BAUD 9600 // BAUD RATE
#define MYUBRR F_CPU/16/BAUD-1 //UBRR

#include <avr/io.h> // Internal Includes
#include <avr/interrupt.h>			
#include <stdio.h>
#include <stdlib.h>
#include <util/delay.h>

//#include "LCD_KPS.h" // External includes
#include "USART_irq.h"

#define LED_ON PORTD |= (1<<PORTD3)
#define LED_OFF PORTD &= ~(1<<PORTD3)
#define LED_Toggle PIND |= (1<<PIND3)


volatile uint32_t accumulator =0; //volatile variables for ISR
volatile uint16_t average =0;
volatile uint16_t samples =0;
volatile uint8_t sendflag=0;

static FILE mystdout = FDEV_SETUP_STREAM(USART0_Transmit_IO,NULL,_FDEV_SETUP_WRITE); 

static uint16_t  temperature;


ISR(ADC_vect)
{
	uint16_t duty= ADC;
	accumulator +=duty;
	samples++;
	if (samples==100)
	{
		average=accumulator/100; //average of 100 values
		accumulator=0;
		samples=0;
		sendflag=1;
	}	
}

ISR(TIMER0_COMPA_vect)
{
	NULL;
}

ISR(TIMER2_OVF_vect)
{
	
	/*
	if (average>43 && average <51)
	{
		LED_ON;
		_delay_ms(20000);
		LED_OFF;
		_delay_ms(5000);
	}
	else if (average>51){
		LED_ON;
		_delay_ms(40000);
		
		_delay_ms(5000);
	}else if(average<38 && average>30){
		LED_OFF;
	}else if(average<30)
	{
		LED_OFF;
	}else{
		LED_OFF;
		
	}
	*/
	NULL;

}
//chrono interrupts

void ADC_init(void)
{
	ADMUX |= (1<<REFS0) | (1<<MUX0); //external capacitor VCC and channel 1
	ADCSRA |= (1<<ADEN)|(1<<ADSC)|(1<<ADATE)|(1<<ADIE)|(1<<ADPS2)|(1<<ADPS1);//enable-start conversion-auto trigger-interrupt enable-64 div factor
	ADCSRB |= (1<<ADTS1) |(1<<ADTS0);// timer counter0 compare match A
	//sei(); //enable interrupts
}

void millisS_10timer(){
	TCCR0A |= (1<<WGM01); //CTC
	TCCR0B |= (1<<CS02) | (1<<CS00); //1024 prescaler
	OCR0A = 154; // 77 -> 10ms x 2 
	TIMSK0 |= (1<<OCIE0A); //enable flag
}

void chrono1_timer()
{
	TCCR2B |= (1<<CS20)|(1<<CS21)|(1<<CS22);
	TIMSK2 |= (1<<TOIE2);
	TCNT2 = 100; //8 bits vreg=256-(fclock*P/prescale) P=1sec
	
}
//chrono definitions
int main(void)
{
	DDRD |= (1<<DDD3) | (1<<DDD5); // set port 3 and 5 as output
	ADC_init(); // adc init
	millisS_10timer(); //timer 0 init
	chrono1_timer();
	USART0_Init(MYUBRR); //USART init
	stdout = &mystdout; //print function
	sei(); //enable interrupts
    /* Replace with your application code */
    while (1) 
    {
		
		if(sendflag) // flag adc == 1 print every second temperature
		{
			temperature = (uint16_t) (((average*4.88)/247.3)-0.011); //adc = 1024*vin/Vref T=vin/S
			printf("%u\n",temperature);
			sendflag=0; //reset flag
		}
		
		
		// GAS (51-43) NO GAS (30-38) GAS	
    }
}


