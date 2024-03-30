package com.social_network.authservice.dto;

import com.social_network.authservice.entity.Role;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
@Builder
public class AuthUserResponseDto {
	private String email;
	private boolean isVerified;
	private Role role;
}
