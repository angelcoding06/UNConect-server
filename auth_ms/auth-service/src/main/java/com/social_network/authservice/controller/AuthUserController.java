package com.social_network.authservice.controller;

import java.util.Map;
import java.util.UUID;
import java.util.logging.Logger;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.social_network.authservice.dto.AuthUserRequestDto;
import com.social_network.authservice.dto.AuthUserResponseDto;
import com.social_network.authservice.dto.TokenDto;
import com.social_network.authservice.entity.AuthUser;
import com.social_network.authservice.entity.LdapUser;
import com.social_network.authservice.service.AuthUserService;
import com.social_network.authservice.service.LdapUserService;
import io.jsonwebtoken.ExpiredJwtException;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;

import org.springframework.amqp.rabbit.core.RabbitTemplate;

@RestController
@PreAuthorize("permitAll()")
@RequestMapping("/auth")
public class AuthUserController {

	Logger logger = Logger.getLogger(getClass().getName());

	@Autowired
	AuthUserService authUserService;

	@Autowired
	LdapUserService ldapUserService;

	@Autowired
	RabbitTemplate rabbitTemplate;

	@GetMapping("/hi")
	public ResponseEntity<String> get() {
		return ResponseEntity.ok("hello");
	}

	@PostMapping("/login")
	public ResponseEntity<TokenDto> login(@RequestBody AuthUserRequestDto dto) {
		TokenDto tokenDto = ldapUserService.authenticate(dto.getEmail(), dto.getPassword())
				? authUserService.login(dto)
				: null;
		if (tokenDto == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(tokenDto);
	}

	@PostMapping("/validate")
	public ResponseEntity<AuthUserResponseDto> validate(@RequestParam String token) {
		AuthUser user = authUserService.validate(token);
		if (user == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(user.toAuthUserResponseDto());
	}

	@PostMapping()
	public ResponseEntity<AuthUserResponseDto> save(@RequestBody AuthUserRequestDto dto) {
		AuthUser authUser = ldapUserService.createUser(dto.getEmail(), dto.getPassword()) != null
				? authUserService.save(dto)
				: null;

		if (authUser == null)
			return ResponseEntity.badRequest().build();
		System.out.println("---------------------------------");
		System.out.println("creado");
		System.out.println("---------------------------------");
		String json = String.format("{\"ID_Auth\":\"%s\"}", authUser.getId());
		rabbitTemplate.convertAndSend("user-queue", json);

		return ResponseEntity.ok(authUser.toAuthUserResponseDto());
	}

	@GetMapping()
	public ResponseEntity<AuthUserResponseDto> get(@RequestBody AuthUserRequestDto dto) {
		AuthUser authUser = authUserService.get(dto);
		if (authUser == null)
			return ResponseEntity.notFound().build();
		return ResponseEntity.ok(authUser.toAuthUserResponseDto());
	}

	@GetMapping("/{id}")
	public ResponseEntity<AuthUserResponseDto> getById(@PathVariable("id") UUID id) {
		AuthUser authUser = authUserService.get(id);
		if (authUser == null)
			return ResponseEntity.notFound().build();
		return ResponseEntity.ok(authUser.toAuthUserResponseDto());
	}


	@PutMapping("/{id}")
	public ResponseEntity<String> update(@PathVariable("id") UUID id,
			@RequestBody AuthUserRequestDto dto) {
		try {
			authUserService.update(id, dto);
			return ResponseEntity.ok().build();
		} catch (Exception e) {
			return ResponseEntity.badRequest().body(e.toString());
		}

	}

	@PatchMapping("/{id}")
	public ResponseEntity<AuthUserResponseDto> updatePatch(@PathVariable("id") UUID id,
			@RequestBody Map<Object, Object> fields) {
		AuthUser authUser = authUserService.patchOne(id, fields);
		if (authUser == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(authUser.toAuthUserResponseDto());
	}

	@DeleteMapping("/{id}")
	public ResponseEntity<AuthUser> delete(@PathVariable("id") UUID id) {
		authUserService.delete(id);
		return ResponseEntity.ok().build();
	}

	@ExceptionHandler(ExpiredJwtException.class)
	public ResponseEntity<String> handleException(ExpiredJwtException ex) {
		return new ResponseEntity<>(ex.getMessage(), HttpStatus.FORBIDDEN);
	}

	@ExceptionHandler(io.jsonwebtoken.security.SignatureException.class)
	public ResponseEntity<String> handleException(io.jsonwebtoken.security.SignatureException ex) {
		return new ResponseEntity<>(ex.getMessage(), HttpStatus.UNAUTHORIZED);
	}

}
