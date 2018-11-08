/*
 * USART_irq.h
 *
 * Created: 15/09/2018 17:57:47
 *  Author: sergi
 */ 


#ifndef USART_IRQ_H_
#define USART_IRQ_H_


/* UART Buffer Defines */
#define USART_RX_BUFFER_SIZE 128     /* 2,4,8,16,32,64,128 or 256 bytes */
#define USART_TX_BUFFER_SIZE 128
#define USART_RX_BUFFER_MASK (USART_RX_BUFFER_SIZE - 1)
#define USART_TX_BUFFER_MASK (USART_TX_BUFFER_SIZE - 1)

/* Prototypes */
void USART0_Init(unsigned int baudrate);
unsigned char USART0_Receive(void);
void USART0_Transmit(unsigned char data);
void USART_putstring(char* StringPtr);
int USART0_Transmit_IO(char data,FILE *stream);

#endif /* USART_IRQ_H_ */