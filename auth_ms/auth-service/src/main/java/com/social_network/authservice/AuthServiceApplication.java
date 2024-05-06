package com.social_network.authservice;

import org.springframework.amqp.core.Queue;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class AuthServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(AuthServiceApplication.class, args);
	}

	@Bean
	public Queue userQueue() {
		Queue queue = new Queue("user-queue");
		System.out.println("Queue 'user-queue' created successfully.");
		return queue;
	}



}
