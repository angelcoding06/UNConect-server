package com.social_network.authservice.service;

import java.lang.reflect.Field;
import java.util.Map;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.ReflectionUtils;
import com.social_network.authservice.dto.AuthUserDto;
import com.social_network.authservice.dto.TokenDto;
import com.social_network.authservice.entity.AuthUser;
import com.social_network.authservice.entity.Role;
import com.social_network.authservice.repository.AuthUserRepository;
import com.social_network.authservice.security.JwtProvider;

@Service
public class AuthUserService {

	@Autowired
	AuthUserRepository authUserRepository;

	@Autowired
	PasswordEncoder passwordEncoder;

	@Autowired
	JwtProvider jwtProvider;

	public AuthUser save(AuthUserDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (user.isPresent())
			return null;
		String password = passwordEncoder.encode(dto.getPassword());
		AuthUser authUser = AuthUser.builder().email(dto.getEmail()).password(password)
				.isVerified(dto.isVerified()).role(dto.getRole()).build();
		return authUserRepository.save(authUser);
	}

	public AuthUser get(AuthUserDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (!user.isPresent())
			return null;
		return user.get();
	}

	public AuthUser update(int id, AuthUserDto dto) {
		Optional<AuthUser> user = authUserRepository.findById(id);
		if (!user.isPresent()) {
			return null;
		}
		AuthUser userToUpdate = user.get();
		boolean emailExists = authUserRepository.findByEmail(dto.getEmail()).isPresent();
		if (emailExists && !dto.getEmail().equals(userToUpdate.getEmail()))
			return null;
		String password = passwordEncoder.encode(dto.getPassword());
		authUserRepository.updateById(dto.getEmail(), password, dto.isVerified(), dto.getRole(),
				id);
		return get(dto);
	}

	public AuthUser patchOne(int id, Map<Object, Object> fields) {
		Optional<AuthUser> user = authUserRepository.findById(id);
		if (user.isPresent()) {
			fields.forEach((key, value) -> {
				if (key == "email") {
					if (emailIsAlreadyUsed((String) value)) {
						return;
					}
				} else if (key == "password") {
					value = passwordEncoder.encode((String) value);
				} else if (key == "role") {
					value = Role.valueOf((String) value);
				}
				Field field = ReflectionUtils.findField(AuthUser.class, (String) key);
				if (field == null)
					return;
				field.setAccessible(true);
				ReflectionUtils.setField(field, user.get(), value);
				field.setAccessible(false);
			});
			return authUserRepository.save(authUserRepository.save(user.get()));
		}
		return null;
	}

	public void delete(int id) {
		authUserRepository.deleteById(id);
	}

	public TokenDto login(AuthUserDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (!user.isPresent())
			return null;
		if (passwordEncoder.matches(dto.getPassword(), user.get().getPassword()))
			return new TokenDto(jwtProvider.createToken(user.get()));
		return null;
	}

	public TokenDto validate(String token) {
		if (!jwtProvider.validate(token))
			return null;
		String email = jwtProvider.getEmailFromToken(token);
		if (!authUserRepository.findByEmail(email).isPresent())
			return null;
		return new TokenDto(token);
	}

	private boolean emailIsAlreadyUsed(String email) {
		return authUserRepository.findByEmail(email).isPresent();
	}
}
