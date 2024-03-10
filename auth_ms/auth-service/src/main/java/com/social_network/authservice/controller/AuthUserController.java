package com.social_network.authservice.controller;

import java.util.Map;
import java.util.logging.Logger;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.social_network.authservice.dto.AuthUserDto;
import com.social_network.authservice.dto.TokenDto;
import com.social_network.authservice.entity.AuthUser;
import com.social_network.authservice.service.AuthUserService;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;


@RestController
@RequestMapping
public class AuthUserController {

	Logger logger = Logger.getLogger(getClass().getName());

	@Autowired
	AuthUserService authUserService;

	@GetMapping("/")
	public String getMethodName() {
		return "hello everybody";
	}


	@PostMapping("/login")
	public ResponseEntity<TokenDto> login(@RequestBody AuthUserDto dto) {
		TokenDto tokenDto = authUserService.login(dto);
		if (tokenDto == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(tokenDto);
	}

	@PostMapping("/validate")
	public ResponseEntity<TokenDto> validate(@RequestParam String token) {
		TokenDto tokenDto = authUserService.validate(token);
		if (tokenDto == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(tokenDto);
	}

	@PostMapping("/create")
	public ResponseEntity<AuthUser> save(@RequestBody AuthUserDto dto) {
		AuthUser authUser = authUserService.save(dto);
		if (authUser == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(authUser);
	}

	@GetMapping("/get")
	public ResponseEntity<AuthUser> get(@RequestBody AuthUserDto dto) {
		AuthUser authUser = authUserService.get(dto);
		if (authUser == null)
			return ResponseEntity.notFound().build();
		return ResponseEntity.ok(authUser);
	}


	@PutMapping("/update/{id}")
	public ResponseEntity<AuthUser> update(@PathVariable("id") int id,
			@RequestBody AuthUserDto dto) {
		AuthUser authUser = authUserService.update(id, dto);
		if (authUser == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(authUser);
	}

	@PatchMapping("/update/{id}")
	public ResponseEntity<AuthUser> updatePatch(@PathVariable("id") int id,
			@RequestBody Map<Object, Object> fields) {
		AuthUser authUser = authUserService.patchOne(id, fields);
		if (authUser == null)
			return ResponseEntity.badRequest().build();
		return ResponseEntity.ok(authUser);
	}

	@DeleteMapping("/delete/{id}")
	public ResponseEntity<AuthUser> delete(@PathVariable("id") int id) {
		authUserService.delete(id);
		return ResponseEntity.ok().build();
	}
}
