package com.social_network.authservice.service;

import java.lang.reflect.Field;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.ReflectionUtils;
import com.social_network.authservice.dto.AuthUserRequestDto;
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

	public AuthUser save(AuthUserRequestDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (user.isPresent())
			return null;
		String password = passwordEncoder.encode(dto.getPassword());
		AuthUser authUser = AuthUser.builder().email(dto.getEmail()).password(password)
				.isVerified(dto.isVerified()).role(dto.getRole()).build();
		return authUserRepository.save(authUser);
	}

	public AuthUser get(AuthUserRequestDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (!user.isPresent())
			return null;
		return user.get();
	}

	public AuthUser get(UUID id) {
		Optional<AuthUser> user = authUserRepository.findById(id);
		if (!user.isPresent())
			return null;
		return user.get();
	}

	public void update(UUID id, AuthUserRequestDto dto) throws Exception {
		Optional<AuthUser> user = authUserRepository.findById(id);
		if (!user.isPresent()) {
			throw new Exception("Nonexistent user");
		}
		AuthUser userToUpdate = user.get();
		boolean emailExists = authUserRepository.findByEmail(dto.getEmail()).isPresent();
		if (emailExists && !dto.getEmail().equals(userToUpdate.getEmail()))
			throw new Exception("email is already used");
		String password = passwordEncoder.encode(dto.getPassword());
		authUserRepository.updateById(dto.getEmail(), password, dto.isVerified(), dto.getRole(),
				id);
	}

	public AuthUser patchOne(UUID id, Map<Object, Object> fields) {
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
			return authUserRepository.save(user.get());
		}
		return null;
	}

	public void delete(UUID id) {
		authUserRepository.deleteById(id);
	}

	public TokenDto login(AuthUserRequestDto dto) {
		Optional<AuthUser> user = authUserRepository.findByEmail(dto.getEmail());
		if (!user.isPresent())
			return null;
		if (passwordEncoder.matches(dto.getPassword(), user.get().getPassword()))
			return new TokenDto(jwtProvider.createToken(user.get()));
		return null;
	}

	public AuthUser validate(String token) {
		if (!jwtProvider.validate(token))
			return null;
		UUID id = UUID.fromString(jwtProvider.getIdFromToken(token));
		Optional<AuthUser> user = authUserRepository.findById(id);
		if (!user.isPresent())
			return null;
		return user.get();
	}

	private boolean emailIsAlreadyUsed(String email) {
		return authUserRepository.findByEmail(email).isPresent();
	}
}
